import os
import signal
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import mlflow
from mlflow.exceptions import MlflowException

from .base_test_mlflow_store_connection import BaseTestMLflowStoreConnection


THIS_DIR = Path(__file__).resolve().parent
TEST_MLFLOW_URI = "http://localhost:6000"


class IntegrationTestMLflowStoreConnection(BaseTestMLflowStoreConnection):
    @classmethod
    def _cleanup_server(cls):
        os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGINT)
        cls.mlflow_server.wait(timeout=10)
        if cls.mlflow_server.returncode is None:
            os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGKILL)

        cls.mlflow_server_data.cleanup()

    # pylint: disable=consider-using-with,subprocess-popen-preexec-fn
    @classmethod
    def setUpClass(cls):
        cls.mlflow_server_data = tempfile.TemporaryDirectory()
        cls.mlflow_server = subprocess.Popen(
            (
                "mlflow",
                "server",
                "--host",
                "127.0.0.1",
                "--port",
                "6000",
                "--backend-store-uri",
                f"sqlite:///{cls.mlflow_server_data.name}/db.sqlite",
                "--artifacts-destination",
                f"{cls.mlflow_server_data.name}/artifacts",
                "--serve-artifacts",
            ),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )

        cls.addClassCleanup(cls._cleanup_server)

        try:
            subprocess.run(
                (
                    "python3",
                    THIS_DIR / "support/integration_test_mlflow_register_models.py",
                    TEST_MLFLOW_URI,
                ),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=THIS_DIR / "support",
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            sys.stdout.buffer.write(exc.output)
            raise unittest.SkipTest(f"{cls.__name__}: failed to upload test model")

        try:
            client = mlflow.tracking.MlflowClient(TEST_MLFLOW_URI)
            client.list_registered_models()
        except MlflowException as exc:
            raise unittest.skipTest(
                f"{cls.__name__}: can't connect to MLflow tracking server at {TEST_MLFLOW_URI}"
            ) from exc

        cls.mlflow_uri = TEST_MLFLOW_URI
        with open(THIS_DIR / "support/hello_world.tflite", "rb") as reference_model:
            cls.reference_model_data = reference_model.read()


del BaseTestMLflowStoreConnection  # don't run base tests
