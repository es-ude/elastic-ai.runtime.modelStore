import hashlib
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
    # pylint: disable=consider-using-with,subprocess-popen-preexec-fn
    @classmethod
    def _start_mlflow_server(cls):
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

    @classmethod
    def _upload_test_models(cls):
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

    @classmethod
    def _cleanup_server(cls):
        os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGINT)
        cls.mlflow_server.wait(timeout=20)
        if cls.mlflow_server.returncode is None:
            os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGKILL)

        cls.mlflow_server_data.cleanup()

    @classmethod
    def _check_server_connection(cls):
        try:
            client = mlflow.tracking.MlflowClient(TEST_MLFLOW_URI)
            client.list_registered_models()
        except MlflowException as exc:
            raise unittest.skipTest(
                f"{cls.__name__}: can't connect to MLflow tracking server at {TEST_MLFLOW_URI}"
            ) from exc

    @classmethod
    def setUpClass(cls):
        cls._start_mlflow_server()
        cls._upload_test_models()
        cls._check_server_connection()

        cls.mlflow_uri = TEST_MLFLOW_URI
        with open(THIS_DIR / "support/hello_world.tflite", "rb") as reference_model:
            cls.reference_model_data = reference_model.read()
            cls.reference_model_hash = hashlib.sha256(cls.reference_model_data).digest()

        url = mlflow.tracking.MlflowClient(TEST_MLFLOW_URI).get_model_version_download_uri(
            "valid_model", "1"
        )
        if url.startswith("mlflow-artifacts"):
            url = mlflow.store.artifact.mlflow_artifacts_repo.MlflowArtifactsRepository.resolve_uri(
                url, TEST_MLFLOW_URI
            )
        cls.reference_model_data_url = f"{url}/model.tflite"


del BaseTestMLflowStoreConnection  # don't run base tests
