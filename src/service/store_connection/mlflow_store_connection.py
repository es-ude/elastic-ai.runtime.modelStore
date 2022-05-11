import mlflow
import tempfile

from pathlib import Path

from service.store_connection import AbstractStoreConnection, ModelNotFound
from service.entities import Model


MODEL_STAGE = "None"


def mlflowFlavorsToFormats(modelPath: str) -> dict:
	model = mlflow.models.Model.load(modelPath)
	flavors = model.get_model_info().flavors
	formats = {}

	if "tensorflow" in flavors:
		formats["tensorflow"] = flavors["tensorflow"]["saved_model_dir"]

	if "keras" in flavors:
		if flavors["keras"]["save_format"] == "tf" and "tensorflow" not in flavors:
			formats["tensorflow"] = flavors["keras"]["data"] + "/model"

	if "tflite" in flavors:
		formats["tflite"] = flavors["tflite"]["data"]

	return formats


def loadModelFiles(path: Path):
	if path.is_file():
		with open(path, "rb") as f:
			return f.read()
	else:
		return {c.name: loadModelFiles(c) for c in path.iterdir()}


class MLflowStoreConnection(AbstractStoreConnection):
	def __init__(self, mlflow_uri: str = "http://localhost:5000"):
		mlflow.set_tracking_uri(mlflow_uri)
		self.client = mlflow.tracking.MlflowClient()

	def getModel(self, modelName: str, version: int = None) -> Model:
		if version == None:
			version = self.getNewestVersion(modelName)

		try:
			uri = self.client.get_model_version_download_uri(modelName, version)
		except mlflow.exceptions.RestException as e:
			raise ModelNotFound from e

		with tempfile.TemporaryDirectory() as tmpDir:
			modelPath = mlflow.artifacts.download_artifacts(artifact_uri=uri, dst_path=tmpDir)

			modelFormats = mlflowFlavorsToFormats(modelPath)
			modelFiles = loadModelFiles(Path(modelPath))

		return Model(modelName, version, modelFormats, modelFiles)

	def getNewestVersion(self, modelName: str) -> int:
		try:
			mvInfos = self.client.get_latest_versions(modelName, [MODEL_STAGE])
		except mlflow.exceptions.RestException as e:
			raise ModelNotFound from e

		try:
			mvInfo = mvInfos[0]
		except IndexError as e:
			raise ModelNotFound from e

		return int(mvInfo.version)
