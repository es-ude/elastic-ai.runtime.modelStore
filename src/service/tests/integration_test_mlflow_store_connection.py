import mlflow
import signal
import subprocess
import sys
import tempfile
import unittest

from mlflow.exceptions import MlflowException
from pathlib import Path
from service.entities import Model
from service.store_connection.mlflow import MLflowStoreConnection, ModelNotFound


THIS_DIR = Path(__file__).resolve().parent
MLFLOW_URI = "http://localhost:5000"


class IntegrationTest_MLflowStoreConnection(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.mlflowServerData = tempfile.TemporaryDirectory()
		cls.mlflowServer = subprocess.Popen(
			("mlflow", "server", "--host", "127.0.0.1", "--backend-store-uri",
				f"sqlite:///{cls.mlflowServerData.name}/db.sqlite", "--artifacts-destination",
				f"{cls.mlflowServerData.name}/artifacts", "--serve-artifacts"),
			stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		cls.addClassCleanup(cls.cleanupServer)

		try:
			subprocess.run(
				("python3", THIS_DIR / "support/integration_test_mlflow_register_models.py"),
				cwd=THIS_DIR / "support", check=True,
				stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as e:
			sys.stdout.buffer.write(e.output)
			raise unittest.SkipTest(f"{cls.__name__}: failed to upload test model")

		try:
			client = mlflow.tracking.MlflowClient(MLFLOW_URI)
			client.list_registered_models()
		except MlflowException as e:
			raise unittest.skipTest(f"{cls.__name__}: can't connect to MLflow tracking server at {MLFLOW_URI}")

	@classmethod
	def cleanupServer(cls):
		cls.mlflowServer.send_signal(signal.SIGINT)
		cls.mlflowServer.wait(timeout=10)
		cls.mlflowServer.kill()

		cls.mlflowServerData.cleanup()

	def setUp(self):
		self.storeConnection = MLflowStoreConnection(MLFLOW_URI)

	def test_getModel(self):
		model = self.storeConnection.getModel("valid_model")
		
		self.assertIsInstance(model, Model)
		self.assertEqual(model.name, "valid_model")
		self.assertEqual(model.version, 2)
		self.assertIn("tflite", model.formats)
		self.assertIn(model.formats["tflite"], model.files)

		with open(THIS_DIR / "support/hello_world.tflite", "rb") as f:
			referenceModelData = f.read()
		
		self.assertEqual(model.files[model.formats["tflite"]], referenceModelData)

	def test_getModel_invalidModel(self):
		self.assertRaises(ModelNotFound, self.storeConnection.getModel, "invalid_model")

	def test_getModel_invalidName(self):
		for v in (None, 1234):
			with self.subTest(v):
				self.assertRaises(TypeError, self.storeConnection.getModel, v)

	def test_getNewestVersion(self):
		version = self.storeConnection.getNewestVersion("valid_model")
		self.assertIsInstance(version, int)
		self.assertEqual(version, 2)

	def test_getNewestVersion_invalidModel(self):
		self.assertRaises(ModelNotFound, self.storeConnection.getNewestVersion, "invalid_model")

	def test_getNewestVersion_invalidName(self):
		for v in (None, 1234):
			with self.subTest(v):
				self.assertRaises(TypeError, self.storeConnection.getNewestVersion, v)
