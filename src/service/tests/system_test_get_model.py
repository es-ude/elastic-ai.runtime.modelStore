import _thread
import time
import unittest
from pathlib import Path

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import requests

import monitor

from .helper_model_store_test import SetUpModelStore


CLIENT_ID = 2
PUBLIC_HOSTNAME = "broker.hivemq.com"
THIS_DIR = Path(__file__).resolve().parent
TEST_MLFLOW_URI = "http://localhost:6000"


class SystemTestGetModel(unittest.TestCase):
    def setUp(self):
        self._monitor = monitor.Monitor(TEST_MLFLOW_URI, None)
        self._received_model = False

    def _start_service(self):
        _thread.start_new_thread(self._monitor.run, ())

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(
            callback,
            "/" + str(CLIENT_ID),
            hostname=PUBLIC_HOSTNAME,
        )

    def _start_client_with_callback(self, callback):
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    def _get_correct_model(self):
        with open(THIS_DIR / "support/hello_world.tflite", "rb") as file:
            model = file.read()
        return model

    def _deliver(self, _client, _userdata, message):
        model_url = message.payload
        res = requests.get(model_url)
        res.raise_for_status()
        correct_model = self._get_correct_model()
        received_model = res.content

        self.assertEqual(correct_model, received_model)
        self._received_model = True
        _thread.exit()

    def _request_model_from_service(self):
        model_name = "model:c67f1c6e5b93d5ee9d9948146357f68c0b28f39f572215f81c191dabda429e10"
        seperator = "$"
        message = str(CLIENT_ID) + seperator + model_name
        publish.single("/service/getModel", message, hostname=PUBLIC_HOSTNAME)

    def _set_up_model_store(self):
        self._model_store = SetUpModelStore()
        self._model_store.set_up()
        self.addClassCleanup(self._model_store.cleanup_server)

    def test_start_monitor_and_send_model_request(self):
        self._set_up_model_store()
        self._start_service()
        self._start_client_with_callback(self._deliver)
        time.sleep(0.5)

        self._request_model_from_service()
        time.sleep(2)
        self.assertTrue(self._received_model)

    def tearDown(self) -> None:
        pass
