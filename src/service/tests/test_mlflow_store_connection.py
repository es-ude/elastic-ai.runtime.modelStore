import sys
from pathlib import Path
from unittest import mock

import mlflow
from mlflow.exceptions import MlflowException

import service
from .base_test_mlflow_store_connection import BaseTestMLflowStoreConnection


class TestMLflowStoreConnection(BaseTestMLflowStoreConnection):
    @classmethod
    def setUpClass(cls):
        mock_mlflow = mock.create_autospec(mlflow)
        cls.addClassCleanup(cls._cleanup_mock)

        def get_latest_versions(model, *_args, **_kwargs):
            if model == "valid_model":
                mock_model_version = mock_mlflow.entities.model_registry.ModelVersion(
                    "valid_model", 2, 0
                )
                mock_model_version.version = 2
                return [mock_model_version]
            else:
                raise MlflowException("")

        mock_mlflow.tracking.MlflowClient().get_latest_versions.side_effect = get_latest_versions

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

        model_info = mock.MagicMock()
        model_info.flavors = {"tflite": {"data": "model.tflite"}}

        mock_mlflow.models.Model.load("").get_model_info.return_value = model_info

        sys.modules["mlflow"] = mock_mlflow
        service.store_connection.mlflow.mlflow = mock_mlflow

        cls.mlflow_uri = "mock-server"
        cls.reference_model_data = b"mock model data"

    @classmethod
    def _cleanup_mock(cls):
        sys.modules["mlflow"] = mlflow
        service.store_connection.mlflow.mlflow = mlflow


del BaseTestMLflowStoreConnection  # don't run base tests
