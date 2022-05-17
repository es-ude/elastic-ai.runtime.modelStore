import mlflow
import service
import sys

from mlflow.exceptions import MlflowException
from pathlib import Path
from unittest import mock

from .base_test_mlflow_store_connection import BaseTest_MLflowStoreConnection


class Test_MLflowStoreConnection(BaseTest_MLflowStoreConnection):
	@classmethod
	def setUpClass(cls):
		mock_mlflow = mock.create_autospec(mlflow)
		cls.addClassCleanup(cls.cleanupMock)

		def get_latest_versions(model, *args, **kwargs):
			if model == "valid_model":
				m = mock_mlflow.entities.model_registry.ModelVersion("valid_model", 2, 0)
				m.version = 2
				return [m]
			else:
				raise MlflowException("")

		mock_mlflow.tracking.MlflowClient().get_latest_versions.side_effect = get_latest_versions

		def download_artifacts(artifact_uri, dst_path, *args, **kwargs):
			path = Path(dst_path)
			model = path / "model"
			model.mkdir()

			with open(model / "MLmodel", "wt") as f:
				f.write("artifact_path: model\n")
				f.write("flavors:\n")
				f.write("  tflite:\n")
				f.write("    data: model.tflite")

			with open(model / "model.tflite", "wb") as f:
				f.write(b"mock model data")

			return str(model)

		mock_mlflow.artifacts.download_artifacts.side_effect = download_artifacts

		model_info = mock.MagicMock()
		model_info.flavors = {"tflite": {"data": "model.tflite"}}

		mock_mlflow.models.Model.load("").get_model_info.return_value = model_info

		sys.modules["mlflow"] = mock_mlflow
		service.store_connection.mlflow.mlflow = mock_mlflow

		cls.mlflowUri = "mock-server"
		cls.referenceModelData = b"mock model data"

	@classmethod
	def cleanupMock(cls):
		sys.modules["mlflow"] = mlflow
		service.store_connection.mlflow.mlflow = mlflow


del BaseTest_MLflowStoreConnection  # don't run base tests
