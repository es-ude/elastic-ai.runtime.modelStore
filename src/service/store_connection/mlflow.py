import tempfile
from pathlib import Path

import mlflow
from mlflow.exceptions import MlflowException

from service.entities import Model


MODEL_STAGE = "None"


class MLflowStoreError(Exception):
    pass


class ModelNotFound(MLflowStoreError):
    pass


class MLflowStoreConnection:
    def _mlflow_flavors_to_formats(self, flavors):
        formats = {}

        if "tensorflow" in flavors:
            formats["tensorflow"] = flavors["tensorflow"]["saved_model_dir"]

        if "keras" in flavors:
            if flavors["keras"]["save_format"] == "tf" and "tensorflow" not in flavors:
                formats["tensorflow"] = flavors["keras"]["data"] + "/model"

        if "tflite" in flavors:
            formats["tflite"] = flavors["tflite"]["data"]

        return formats

    def _load_formats_from_mlflow_model(self, model_path):
        model = mlflow.models.Model.load(model_path)
        flavors = model.get_model_info().flavors
        return self._mlflow_flavors_to_formats(flavors)

    def _load_model_files(self, path):
        if not isinstance(path, Path):
            path = Path(path)

        if path.is_file():
            with open(path, "rb") as file:
                return file.read()
        else:
            return {child.name: self._load_model_files(child) for child in path.iterdir()}

    def __init__(self, mlflow_uri):
        mlflow.set_tracking_uri(mlflow_uri)
        self.client = mlflow.tracking.MlflowClient()

    def get_model(self, model_name: str) -> Model:
        if not isinstance(model_name, str):
            raise TypeError("modelName")

        # will raise ModelNotFound
        version = self.get_newest_version(model_name)

        uri = self.client.get_model_version_download_uri(model_name, version)

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_path = mlflow.artifacts.download_artifacts(artifact_uri=uri, dst_path=tmp_dir)

            model_formats = self._load_formats_from_mlflow_model(model_path)
            model_files = self._load_model_files(model_path)

        return Model(model_name, version, model_formats, model_files)

    def get_newest_version(self, model_name: str) -> int:
        if not isinstance(model_name, str):
            raise TypeError("modelName")

        try:
            model_versions = self.client.get_latest_versions(model_name, [MODEL_STAGE])
        except MlflowException as exc:
            raise ModelNotFound from exc

        try:
            model_version = model_versions[0]
        except IndexError as exc:
            raise MLflowStoreError from exc

        return int(model_version.version)
