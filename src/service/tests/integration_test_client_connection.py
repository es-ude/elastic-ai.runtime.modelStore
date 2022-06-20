import _thread
import time
import unittest
import threading

from paho.mqtt import subscribe

from service.client_connection import ClientConnection
from service.mocks import MockServiceCommands, MockModel


NODE_ID = 1
MODEL_NOT_FOUND_ERROR = b"1"
HOSTNAME= "broker.hivemq.com"


class IntegrationTestClientConnection(unittest.TestCase):
    def setUp(self) -> None:
        self._service_commands = MockServiceCommands()
        self._client = ClientConnection(NODE_ID, self._service_commands)
        self._model = MockModel()
        self._verified = False

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(callback, "/"+str(NODE_ID), hostname=HOSTNAME)

    def _deliver(self, client, userdata, message):
        self.assertEquals(message.payload, b'0')        #mock service commands sends b'0' as model
        self._veryfied = True
        _thread.exit()

    def _deliver_model_not_found(self, client, userdata, message):
        self.assertEqual(message.payload, MODEL_NOT_FOUND_ERROR)
        self._verified = True
        _thread.exit()

    def _start_client_with_callback(self, callback):
        #return threading.Thread(target=self._subscribe_to_public_broker, args=(callback,))
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    #Tests if a served model can be received
    def test_serve_empty_model(self):
        self._start_client_with_callback(self._deliver)
        #clientThread.start()
        time.sleep(0.5)

        self._client.serve_model(self._model.formats["tflite"])

    def test_client_receives_error_after_requesting_unknown_model(self):
        self._start_client_with_callback(self._deliver_model_not_found)
        #clientThread.start()
        time.sleep(0.5)

        self._client.get_and_serve_model("unknown_model")
        time.sleep(0.5)
        self.assertTrue(self._verified)

    def tearDown(self):
        self._verified = False
