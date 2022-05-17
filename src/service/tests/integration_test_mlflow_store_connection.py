import mlflow
import signal
import subprocess
import sys
import tempfile
import unittest

from mlflow.exceptions import MlflowException
from pathlib import Path

from .base_test_mlflow_store_connection import BaseTest_MLflowStoreConnection


THIS_DIR = Path(__file__).resolve().parent
MLFLOW_URI = "http://localhost:6000"


class IntegrationTest_MLflowStoreConnection(BaseTest_MLflowStoreConnection):
	@classmethod
	def setUpClass(cls):
		cls.mlflowServerData = tempfile.TemporaryDirectory()
		cls.mlflowServer = subprocess.Popen(
			("mlflow", "server", "--host", "127.0.0.1", "--port", "6000", "--backend-store-uri",
				f"sqlite:///{cls.mlflowServerData.name}/db.sqlite", "--artifacts-destination",
				f"{cls.mlflowServerData.name}/artifacts", "--serve-artifacts"),
			stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		cls.addClassCleanup(cls.cleanupServer)

		try:
			subprocess.run(
				("python3", THIS_DIR / "support/integration_test_mlflow_register_models.py", MLFLOW_URI),
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

		cls.mlflowUri = MLFLOW_URI
		with open(THIS_DIR / "support/hello_world.tflite", "rb") as f:
			cls.referenceModelData = f.read()

	@classmethod
	def cleanupServer(cls):
		cls.mlflowServer.send_signal(signal.SIGINT)
		cls.mlflowServer.wait(timeout=10)
		cls.mlflowServer.kill()

		cls.mlflowServerData.cleanup()


del BaseTest_MLflowStoreConnection  # don't run base tests
