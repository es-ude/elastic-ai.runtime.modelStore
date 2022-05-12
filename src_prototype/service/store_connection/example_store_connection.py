from service.store_connection import AbstractStoreConnection, ModelNotFound
from service.entities import Model


class ExampleModelStore:
	def __init__(self):
		self._models = {}
		self.storeModel(Model("hello_world", 1, {"tflite": "model.tflite"}, {"model.tflite": b"<Model data...>"}))
		self.storeModel(Model("test_model", 1, {"tflite": "model.tflite"}, {"model.tflite": b"<Model data...>"}))
		self.storeModel(Model("test_model", 2, {"tflite": "model.tflite"}, {"model.tflite": b"<Model data...>"}))
		self.storeModel(Model("multi_format", 1, {"tflite": "model.tflite", "tensorflow": "tf_model"}, {
			"model.tflite": b"<Model data in tflite format...>",
			"tf_model": {"saved_model.pb": b"<Model data in SavedModel format...>", "assets": {}, "variables": {}}
		}))

	def storeModel(self, model: Model):
		self._models.setdefault(model.name, {})[model.version] = model

	def getModel(self, modelName: str, version: int = None) -> Model:
		try:
			versions = self._models[modelName]
		except KeyError:
			return None

		try:
			if version == None:
				version = max(versions)

			return versions[version]
		except KeyError:
			return None

	def getNewestVersion(self, modelName: str) -> int:
		try:
			versions = self._models[modelName]
		except KeyError:
			return None

		return max(versions)


class ExampleStoreConnection(AbstractStoreConnection):
	def __init__(self):
		self._store = ExampleModelStore()

	def getModel(self, modelName: str, version: int = None) -> Model:
		model = self._store.getModel(modelName, version)
		if model == None:
			raise ModelNotFound

		return model

	def getNewestVersion(self, modelName: str) -> int:
		newestVersion = self._store.getNewestVersion(modelName)
		if newestVersion == None:
			raise ModelNotFound

		return newestVersion
