FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /mlflow-data

ENTRYPOINT ["mlflow", "server"]
CMD ["--host", "0.0.0.0", "--backend-store-uri", "sqlite:////mlflow-data/db.sqlite", "--artifacts-destination", "/mlflow-data/artifacts", "--serve-artifacts"]
