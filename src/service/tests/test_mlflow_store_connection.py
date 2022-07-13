import hashlib
from pathlib import Path
from unittest import mock

import mlflow
import requests
import yaml

import service

from .base_test_mlflow_store_connection import BaseTestMLflowStoreConnection


class TestMLflowStoreConnection(BaseTestMLflowStoreConnection):
    @classmethod
    def setUpClass(cls):
        cls.mlflow_uri = "http://mock-server"
        cls.reference_model_data = b"mock model data"
        cls.reference_model_data_url = "http://example.com/model/model.tflite"
        cls.reference_model_hash = hashlib.sha256(cls.reference_model_data).digest()

        mock_mlflow = mock.create_autospec(mlflow)
        cls.addClassCleanup(cls._cleanup_mock)

        def search_model_versions(*_args, **_kwargs):
            mock_model_version = mock_mlflow.entities.model_registry.ModelVersion(
                "valid_model", 2, 0
            )
            mock_model_version.name = "valid_model"
            mock_model_version.version = 1
            mock_model_version.tags = {"hash": cls.reference_model_hash.hex()}
            return [mock_model_version]

        mock_mlflow.tracking.MlflowClient().search_model_versions.side_effect = (
            search_model_versions
        )

        def download_artifacts(dst_path, *_args, **_kwargs):
            path = Path(dst_path)
            model = path / "model"
            model.mkdir()

            with open(model / "MLmodel", "wt") as file:
                file.write("artifact_path: model\n")
                file.write("flavors:\n")
                file.write("  tflite:\n")
                file.write("    data: model.tflite")

            with open(model / "model.tflite", "wb") as file:
                file.write(b"mock model data")

            return str(model)

        mock_mlflow.artifacts.download_artifacts.side_effect = download_artifacts

        def get_model_version_download_uri(*_args, **_kwargs):
            return "http://example.com/model"

        mock_mlflow.tracking.MlflowClient().get_model_version_download_uri.side_effect = (
            get_model_version_download_uri
        )

        model_info = mock.MagicMock()
        model_info.flavors = {"tflite": {"data": "model.tflite"}}

        mock_mlflow.models.Model.from_dict({}).get_model_info.return_value = model_info

        service.store_connection.mlflow.mlflow = mock_mlflow
        service.store_connection.mlflow.requests = mock.MagicMock()
        service.store_connection.mlflow.yaml = mock.MagicMock()

    @classmethod
    def _cleanup_mock(cls):
        service.store_connection.mlflow.mlflow = mlflow
        service.store_connection.mlflow.requests = requests
        service.store_connection.mlflow.yaml = yaml


del BaseTestMLflowStoreConnection  # don't run base tests
