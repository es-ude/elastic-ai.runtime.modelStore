#!/usr/bin/env sh

if ! python3 -c "import mlflow"; then
   pip3 install -r requirements.txt
fi

mkdir -p ./mlflow-data
mlflow server --host ${1:-127.0.0.1} --backend-store-uri sqlite:///mlflow-data/db.sqlite \
   --artifacts-destination ./mlflow-data/artifacts --serve-artifacts
