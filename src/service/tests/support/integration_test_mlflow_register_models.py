import mlflow
import mlflow_tflite
import sys


mlflow.set_tracking_uri(sys.argv[1])

with open("hello_world.tflite", "rb") as f:
   model = f.read()

REG_MODEL_NAME = "valid_model"

mlflow_tflite.log_model(model, "model", registered_model_name="valid_model")
mlflow_tflite.log_model(model, "model", registered_model_name="valid_model")
