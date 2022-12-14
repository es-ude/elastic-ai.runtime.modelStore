import hashlib
from urllib.parse import urlparse, urlunparse

import mlflow
import requests
import yaml
from mlflow.store.artifact.mlflow_artifacts_repo import MlflowArtifactsRepository

from service.entities import Model
from service.errors import IllegalInput, ModelDataNotFound


MODEL_STAGE = "None"


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

    def _get_format_and_data_url(self, artifact_url: str):
        res = requests.get(f"{artifact_url}/MLmodel")
        res.raise_for_status()
        model_info = yaml.safe_load(res.content)

        model = mlflow.models.Model.from_dict(model_info)
        flavors = model.get_model_info().flavors
        path_and_format = self._get_model_data_path_and_format(flavors)
        if path_and_format is None:
            raise ModelDataNotFound("Model has no supported format")

        path, model_format = path_and_format
        return f"{artifact_url}/{path}", model_format

    def _resolve_artifact_uri(self, artifact_uri):
        uri = MlflowArtifactsRepository.resolve_uri(artifact_uri, mlflow.get_tracking_uri())
        if self.mlflow_public_netloc is not None:
            uri = urlparse(uri)
            uri = uri._replace(netloc=self.mlflow_public_netloc)
            uri = urlunparse(uri)
        return uri

    def __init__(self, mlflow_uri, mlflow_public_uri):
        mlflow.set_tracking_uri(mlflow_uri)

        if mlflow_public_uri is not None:
            self.mlflow_public_netloc = urlparse(mlflow_public_uri).netloc
        else:
            self.mlflow_public_netloc = None

        self.client = mlflow.tracking.MlflowClient()

    def get_model(self, model_hash: bytes) -> Model:
        if not isinstance(model_hash, bytes):
            raise TypeError("model_hash")
        if len(model_hash) != hashlib.sha256().digest_size:
            raise IllegalInput("model_hash")

        all_versions = self.client.search_model_versions("")
        matching_versions = [
            v for v in all_versions if bytes.fromhex(v.tags.get("hash", "")) == model_hash
        ]

        if len(matching_versions) == 0:
            raise ModelDataNotFound
        if len(matching_versions) > 1:
            print(
                f"The store contains more than one model with the hash '{model_hash.hex()}', using the first model found"
            )

        version = matching_versions[0]
        uri = self.client.get_model_version_download_uri(version.name, version.version)
        if uri.startswith("mlflow-artifacts"):
            uri = self._resolve_artifact_uri(uri)

        data_url, model_format = self._get_format_and_data_url(uri)
        return Model(version.name, int(version.version), model_format, data_url)

    def get_all_graphs(self) -> list[str]:
        all_versions = self.client.search_model_versions("")
        all_graphs = [v.tags.get("graph") for v in all_versions if v.tags.get("graph") is not None]
        return all_graphs
