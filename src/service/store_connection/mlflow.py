import hashlib
import tempfile
from pathlib import Path
from urllib.parse import urlparse

import mlflow
from mlflow.exceptions import MlflowException

from service.entities import Model


MODEL_STAGE = "None"


class MLflowStoreError(Exception):
    pass


class ModelNotFound(MLflowStoreError):
    pass


class MLflowStoreConnection:
    def _get_model_data_path_and_format(self, flavors):
        if "tensorflow" in flavors:
            return flavors["tensorflow"]["saved_model_dir"], "tensorflow"

        if "keras" in flavors:
            if flavors["keras"]["save_format"] == "tf" and "tensorflow" not in flavors:
                return flavors["keras"]["data"] + "/model", "tensorflow"

        if "tflite" in flavors:
            return flavors["tflite"]["data"], "tflite"

        return None

    def _load_model_files(self, path: Path):
        if path.is_file():
            with open(path, "rb") as file:
                return file.read()
        else:
            return {child.name: self._load_model_files(child) for child in path.iterdir()}

    def _load_data_from_mlflow_model(self, model_path: Path):
        model = mlflow.models.Model.load(str(model_path))
        flavors = model.get_model_info().flavors
        path_and_format = self._get_model_data_path_and_format(flavors)
        if path_and_format is None:
            raise ModelNotFound("Model has no supported format")

        path, model_format = path_and_format
        return self._load_model_files(model_path / path), model_format

    def __init__(self, mlflow_uri):
        mlflow.set_tracking_uri(mlflow_uri)
        self.client = mlflow.tracking.MlflowClient()

    def get_model(self, model_hash: bytes) -> Model:
        if not isinstance(model_hash, bytes):
            raise TypeError("model_hash")
        if len(model_hash) != hashlib.sha256().digest_size:
            raise ValueError("model_hash")

        all_versions = self.client.search_model_versions("")
        matching_versions = [v for v in all_versions if bytes.fromhex(v.tags.get("hash", "")) == model_hash]

        if len(matching_versions) == 0:
            raise ModelNotFound
        if len(matching_versions) > 1:
            print(f"The store contains more than one model with the hash '{model_hash.hex()}', using the first model found")

        version = matching_versions[0]
        uri = self.client.get_model_version_download_uri(version.name, version.version)

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_path = mlflow.artifacts.download_artifacts(artifact_uri=uri, dst_path=tmp_dir)
            data, model_format = self._load_data_from_mlflow_model(Path(model_path))

        return Model(version.name, int(version.version), model_format, data)
