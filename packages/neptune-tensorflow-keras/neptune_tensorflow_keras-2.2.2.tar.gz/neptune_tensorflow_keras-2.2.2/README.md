# Neptune + Keras integration

Experiment tracking for Keras-trained models.

## What will you get with this integration?

* Log, organize, visualize, and compare ML experiments in a single place
* Monitor model training live
* Version and query production-ready models and associated metadata (e.g., datasets)
* Collaborate with the team and across the organization

## What will be logged to Neptune?

* hyperparameters for every run,
* learning curves for losses and metrics during training,
* hardware consumption and stdout/stderr output during training,
* TensorFlow tensors as images to see model predictions live,
* training code and Git commit information,
* model weights,
* [other metadata](https://docs.neptune.ai/logging/what_you_can_log)

![image](https://docs.neptune.ai/img/app/integrations/keras.png)
*Example charts in the Neptune UI with logged accuracy and loss*

## Resources

* [Documentation](https://docs.neptune.ai/integrations/keras)
* [Code example on GitHub](https://github.com/neptune-ai/examples/blob/main/integrations-and-supported-tools/tensorflow-keras/scripts)
* [Runs logged in the Neptune app](https://app.neptune.ai/o/common/org/tf-keras-integration/e/TFK-18/all)
* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/master/integrations-and-supported-tools/tensorflow-keras/notebooks/Neptune_TensorFlow_Keras.ipynb)

## Example

On the command line:

```
pip install neptune-tensorflow-keras
```

In Python:

```python
import neptune
from neptune.integrations.tensorflow_keras import NeptuneCallback
from neptune import ANONYMOUS_API_TOKEN

# Start a run
run = neptune.init_run(
    project="common/tf-keras-integration",
    api_token=ANONYMOUS_API_TOKEN,
)

# Create a NeptuneCallback instance
neptune_cbk = NeptuneCallback(run=run, base_namespace="metrics")

# Pass the callback to model.fit()
model.fit(
    x_train,
    y_train,
    epochs=5,
    batch_size=64,
    callbacks=[neptune_cbk],
)

# Stop the run
run.stop()
```

## Support

If you got stuck or simply want to talk to us, here are your options:

* Check our [FAQ page](https://docs.neptune.ai/getting_help)
* You can submit bug reports, feature requests, or contributions directly to the repository.
* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),
* You can just shoot us an email at support@neptune.ai
