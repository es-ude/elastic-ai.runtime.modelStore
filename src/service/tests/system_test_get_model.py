import unittest
import monitor
import threading
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
from .helper_model_store_test import SetUpModelStore
from pathlib import Path
import _thread

NODE_ID = 1
PUBLIC_HOSTNAME = "broker.hivemq.com"
THIS_DIR = Path(__file__).resolve().parent
TEST_MLFLOW_URI = "http://localhost:6000"

class SystemTestGetModel(unittest.TestCase):
    def setUp(self):
        self._monitor = monitor.Monitor(TEST_MLFLOW_URI, PUBLIC_HOSTNAME)
        self._received_model = False

    def _start_service(self):
        _thread.start_new_thread(self._monitor.run, ())

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(callback, "/"+str(NODE_ID), hostname=PUBLIC_HOSTNAME, )

    def _start_client_with_callback(self, callback):
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    def _get_correct_model(self):
        with open("service/tests/support/hello_world.tflite", "rb") as file:
            model = file.read()
        return model

    def _deliver(self, client, userdata, message):
        correct_model = self._get_correct_model()
        received_model = message.payload

        self.assertEqual(correct_model, received_model)
        self._received_model = True
        _thread.exit()

    def _request_model_from_service(self):
        model_name = "valid_model"
        seperator = "$"
        message = str(NODE_ID)+seperator+model_name
        publish.single("/service/getModel", message, hostname=PUBLIC_HOSTNAME)

    def _set_up_model_store(self):
        self._model_store = SetUpModelStore()
        self._model_store.set_up()
        self.addClassCleanup(self._model_store.cleanup_server)

    def test_start_monitor_and_send_request(self):
        self._set_up_model_store()
        self._start_service()
        self._start_client_with_callback(self._deliver)
        time.sleep(0.5)

        self._request_model_from_service()
        time.sleep(0.5)
        self.assertTrue(self._received_model)

    def tearDown(self) -> None:
        pass
