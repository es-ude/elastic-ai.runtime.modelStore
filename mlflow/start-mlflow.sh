#!/usr/bin/env sh

if ! python -c "import mlflow"; then
   pip install -r requirements.txt
fi

mkdir -p ./mlflow-data
mlflow server --host 127.0.0.1 --backend-store-uri sqlite:///mlflow-data/db.sqlite \
   --artifacts-destination ./mlflow-data/artifacts --serve-artifacts