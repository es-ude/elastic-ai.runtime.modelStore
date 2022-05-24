import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

import mlflow
from mlflow.exceptions import MlflowException


THIS_DIR = Path(__file__).resolve().parent
TEST_MLFLOW_URI = "http://localhost:6000"


class SetUpModelStore():
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

    @classmethod
    def _upload_test_models(cls):
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


    @classmethod
    def cleanup_server(cls):
        os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGINT)
        cls.mlflow_server.wait(timeout=10)
        if cls.mlflow_server.returncode is None:
            os.killpg(os.getpgid(cls.mlflow_server.pid), signal.SIGKILL)

        cls.mlflow_server_data.cleanup()

    @classmethod
    def _check_server_connection(cls):
        client = mlflow.tracking.MlflowClient(TEST_MLFLOW_URI)
        client.list_registered_models()

    @classmethod
    def set_up(cls):
        cls._start_mlflow_server()
        cls._upload_test_models()
        cls._check_server_connection()

        cls.mlflow_uri = TEST_MLFLOW_URI
