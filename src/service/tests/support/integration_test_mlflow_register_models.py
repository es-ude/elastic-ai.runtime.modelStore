import sys

import mlflow

import mlflow_tflite
import model_store_client as msc

mlflow.set_tracking_uri(sys.argv[1])

with open("hello_world.tflite", "rb") as file:
    model = file.read()

mlflow.log_metric("mae", 0.295)
msc.log_predicate(msc.ServiceNamespace.Predict, msc.ServiceNamespace.Sine)
msc.log_predicate(msc.ServiceNamespace.Input, msc.ServiceNamespace.Float)
msc.log_predicate(msc.ServiceNamespace.Output, msc.ServiceNamespace.Float)
model_info = mlflow_tflite.log_model(model, "model")
msc.register_model(model_info.model_uri, "valid_model")
