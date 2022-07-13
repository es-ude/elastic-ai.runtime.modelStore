#!/usr/bin/env sh

isort --profile black --atomic --lines-after-imports 2 -l 100 --thirdparty mlflow \
    --project mlflow_tflite --project model_store_client mlflow/ src/
black -l 100 mlflow/ src/
