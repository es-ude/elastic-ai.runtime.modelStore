import tempfile
import mlflow

from mlflow.exceptions import MlflowException, RestException
from pathlib import Path
from service.entities import Model


MODEL_STAGE = "None"


class MLflowStoreError(Exception): pass
class ModelNotFound(MLflowStoreError): pass


class MLflowStoreConnection:
	def _mlflowFlavorsToFormats(self, flavors):
		formats = {}

		if "tensorflow" in flavors:
			formats["tensorflow"] = flavors["tensorflow"]["saved_model_dir"]

		if "keras" in flavors:
			if flavors["keras"]["save_format"] == "tf" and "tensorflow" not in flavors:
				formats["tensorflow"] = flavors["keras"]["data"] + "/model"

		if "tflite" in flavors:
			formats["tflite"] = flavors["tflite"]["data"]

		return formats

	def _loadFormatsFromMLflowModel(self, modelPath):
		model = mlflow.models.Model.load(modelPath)
		flavors = model.get_model_info().flavors
		return self._mlflowFlavorsToFormats(flavors)

	def _loadModelFiles(self, path):
		if not isinstance(path, Path):
			path = Path(path)
		
		if path.is_file():
			with open(path, "rb") as f:
				return f.read()
		else:
			return {child.name: self._loadModelFiles(child) for child in path.iterdir()}

	def __init__(self, mlflowUri):
		mlflow.set_tracking_uri(mlflowUri)
		self.client = mlflow.tracking.MlflowClient()

	def getModel(self, modelName: str) -> Model:
		if not isinstance(modelName, str):
			raise TypeError("modelName")

		# will raise ModelNotFound
		version = self.getNewestVersion(modelName)
		
		uri = self.client.get_model_version_download_uri(modelName, version)

		with tempfile.TemporaryDirectory() as tmpDir:
			modelPath = mlflow.artifacts.download_artifacts(artifact_uri=uri, dst_path=tmpDir)

			modelFormats = self._loadFormatsFromMLflowModel(modelPath)
			modelFiles = self._loadModelFiles(modelPath)

		return Model(modelName, version, modelFormats, modelFiles)

	def getNewestVersion(self, modelName: str) -> int:
		if not isinstance(modelName, str):
			raise TypeError("modelName")

		try:
			mvInfos = self.client.get_latest_versions(modelName, [MODEL_STAGE])
		except MlflowException as e:
			raise ModelNotFound from e
		
		try:
			mvInfo = mvInfos[0]
		except IndexError as e:
			raise MLflowStoreError from e
		
		return int(mvInfo.version)
