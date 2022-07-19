import mlflow

import mlflow_tflite
import model_store_client as msc


# start mlflow run

mlflow.set_tracking_uri("http://localhost:5000")

# load existing model

with open("hello_world.tflite", "rb") as f:
    model = f.read()

# log and register model

REG_MODEL_NAME = "existing_hello_world"

msc.log_predicate(msc.ServiceNamespace.Predict, msc.ServiceNamespace.Digits)
msc.log_predicate(msc.ServiceNamespace.Input, msc.ServiceNamespace.Float)
msc.log_predicate(msc.ServiceNamespace.Output, msc.ServiceNamespace.Float)
model_info = mlflow_tflite.log_model(model, "model")
msc.register_model(model_info.model_uri, REG_MODEL_NAME)
