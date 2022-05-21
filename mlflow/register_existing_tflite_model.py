import mlflow

import mlflow_tflite


# start mlflow run

mlflow.set_tracking_uri("http://localhost:5000")

# load existing model

with open("hello_world.tflite", "rb") as f:
    model = f.read()

# log and register model

REG_MODEL_NAME = "hello_world"

mlflow_tflite.log_model(model, "model", registered_model_name=REG_MODEL_NAME)
