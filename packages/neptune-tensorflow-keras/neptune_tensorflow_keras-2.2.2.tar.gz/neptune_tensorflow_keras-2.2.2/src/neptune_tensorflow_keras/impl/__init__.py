#
# Copyright (c) 2021, Neptune Labs Sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__all__ = ["__version__", "NeptuneCallback"]

import io
import tempfile
import warnings
from typing import Union

# Note: we purposefully try to import `tensorflow.keras.callbacks.Callback`
# before `keras.callbacks.Callback` because the former is compatible with both
# `tensorflow.keras` and `keras`, while the latter is only compatible
# with `keras`. See https://github.com/keras-team/keras/issues/14125

try:
    from tensorflow.keras.callbacks import Callback
    from tensorflow.keras.utils import model_to_dot
except ImportError as exc:
    try:
        from keras.callbacks import Callback
        from keras.utils import model_to_dot
    except ImportError:
        msg = """
        keras package not found.

        As Keras is now part of Tensorflow you should install it by running
            pip install tensorflow"""
        raise ModuleNotFoundError(msg) from exc

from neptune_tensorflow_keras.impl.version import __version__

try:
    # neptune-client>=1.0.0 package structure
    import neptune
    from neptune.exceptions import NeptuneException
    from neptune.integrations.utils import (
        expect_not_an_experiment,
        verify_type,
    )
    from neptune.types import File
    from neptune.utils import stringify_unsupported
except ImportError:
    # neptune-client=0.9.0+ package structure
    import neptune.new as neptune
    from neptune.new.exceptions import NeptuneException
    from neptune.new.integrations.utils import (
        expect_not_an_experiment,
        verify_type,
    )
    from neptune.new.types import File
    from neptune.new.utils import stringify_unsupported


INTEGRATION_VERSION_KEY = "source_code/integrations/neptune-tensorflow-keras"


class NeptuneCallback(Callback):
    """Captures model training metadata and logs them to Neptune.

    Note: To use this module, you need to have Keras or Tensorflow 2 installed.

    Args:
        run: Neptune run object. You can also pass a namespace handler object;
            for example, run["test"], in which case all metadata is logged under
            the "test" namespace inside the run.
        base_namespace: Namespace where all metadata logged by the callback is stored.
        log_on_batch: Whether to log the metrics also for each batch, not only each epoch.
        log_model_diagram: Whether to save the model visualization.
            Requires pydot to be installed: https://pypi.org/project/pydot/
        log_model_summary: Whether to log the model summary.

    Example:
        import neptune
        from neptune.integrations.tensorflow_keras import NeptuneCallback

        run = neptune.init_run()
        neptune_callback = NeptuneCallback(run=run)
        model.fit(x_train, y_train, callbacks=[neptune_callback])

    For more, see the docs:
        Tutorial: https://docs.neptune.ai/integrations/keras/
        API reference: https://docs.neptune.ai/api/integrations/keras/
    """

    def __init__(
        self,
        run: Union[neptune.Run, neptune.handler.Handler],
        base_namespace: str = "training",
        log_model_diagram: bool = False,
        log_on_batch: bool = False,
        log_model_summary: bool = True,
    ):
        super().__init__()

        expect_not_an_experiment(run)
        verify_type("run", run, (neptune.Run, neptune.handler.Handler))
        verify_type("base_namespace", base_namespace, str)
        verify_type("log_model_diagram", log_model_diagram, bool)
        verify_type("log_model_summary", log_model_summary, bool)

        self._run = run
        self._log_model_diagram = log_model_diagram
        self._log_on_batch = log_on_batch
        self._log_model_summary = log_model_summary

        if base_namespace.endswith("/"):
            self._base_namespace = base_namespace[:-1]
        else:
            self._base_namespace = base_namespace

        root_obj = self._run
        if isinstance(self._run, neptune.handler.Handler):
            root_obj = self._run.get_root_object()

        root_obj[INTEGRATION_VERSION_KEY] = __version__

    @property
    def _metric_logger(self):
        return self._run[self._base_namespace]

    @property
    def _model_logger(self):
        return self._run[self._base_namespace]["model"]

    def _log_metrics(self, logs, category: str, trigger: str):
        if not logs:
            return

        logger = self._metric_logger[category][trigger]

        for metric, value in logs.items():
            try:
                if metric in ("batch", "size") or metric.startswith("val_"):
                    continue
                logger[metric].append(value)
            except NeptuneException:
                pass

    def on_train_begin(self, logs=None):
        optimizer_config = self.model.optimizer.get_config()  # it is a dict
        self._model_logger["optimizer_config"] = stringify_unsupported(optimizer_config)
        self._metric_logger["fit_params"] = self.params

    def on_train_end(self, logs=None):
        # We need this to be logged at the end of the training, otherwise we are risking this to happen:
        # https://stackoverflow.com/q/55908188/3986320
        if self._log_model_summary:
            try:
                self._model_logger["summary"] = _model_summary_file(self.model)
            except ValueError as e:
                warnings.warn(f"Model summary not logged. {e}", category=RuntimeWarning)

        if self._log_model_diagram:
            try:
                self._model_logger["visualization"] = _model_diagram(self.model)
            except ValueError as e:
                warnings.warn(f"Model visualization not logged. {e}", category=RuntimeWarning)

    def on_train_batch_end(self, batch, logs=None):
        if self._log_on_batch:
            self._log_metrics(logs, "train", "batch")

    def on_epoch_begin(self, epoch, logs=None):
        self._model_logger["learning_rate"].append(self.model.optimizer.learning_rate.numpy())

    def on_epoch_end(self, epoch, logs=None):
        self._log_metrics(logs, "train", "epoch")

    def on_test_batch_end(self, batch, logs=None):
        if self._log_on_batch:
            self._log_metrics(logs, "validation", "batch")

    def on_test_end(self, logs=None):
        self._log_metrics(logs, "validation", "epoch")


def _model_summary_file(model) -> File:
    stream = io.StringIO()
    model.summary(print_fn=lambda x, **kwargs: stream.write(x + "\n"))
    return File.from_stream(stream, extension="txt")


def _model_diagram(model) -> File:
    dot = model_to_dot(model)
    if dot is not None:
        # the same as TF/Keras does, we will fail with ImportError unless using a notebook,
        # where it just prints a warning message
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        dot.write(tmp.name, format="png")
        return File(tmp.name)
