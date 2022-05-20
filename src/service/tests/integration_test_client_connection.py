import _thread
import time
import unittest

from paho.mqtt import subscribe

from service.client_connection import ClientConnection
from service.mocks import MockServiceCommands, MockModel


NODE_ID = 1
MODEL_NOT_FOUND_ERROR = b"1"


class IntegrationTestClientConnection(unittest.TestCase):
    def setUp(self) -> None:
        self._service_commands = MockServiceCommands()
        self._client = ClientConnection(NODE_ID, self._service_commands)
        self._model = MockModel()
        self._verified = False

    def _subscribe_helper(self):
        subscribe.callback(self._deliver, "/" + str(NODE_ID), hostname="broker.hivemq.com")

    def _deliver(self, _client, _userdata, message):
        self.assertEqual(message.payload, b"0")  # mock service commands sends b'0' as model
        self._verified = True
        _thread.exit()

    def _subscribe_helper_model_not_found(self):
        subscribe.callback(
            self._deliver_model_not_found, "/" + str(NODE_ID), hostname="broker.hivemq.com"
        )

    def _deliver_model_not_found(self, _client, _userdata, message):
        self.assertEqual(message.payload, MODEL_NOT_FOUND_ERROR)
        self._verified = True
        _thread.exit()

    # Tests if a served model can be received
    def test_serve_empty_model(self):

        # Subscribe to topic /1
        _thread.start_new_thread(self._subscribe_helper, ())
        time.sleep(0.5)  # Problem: Nach F.I.R.S.T Prinzip müssen Tests immer schnell sein.

        self._client.serve_model(self._model.formats["tflite"])

        time.sleep(0.5)
        self.assertTrue(self._verified)

    # tell the client, that the wanted model could not be found
    def test_model_not_found(self):
        _thread.start_new_thread(self._subscribe_helper_model_not_found, ())
        time.sleep(0.5)

        self._client.get_and_serve_model("unknown_model")
        time.sleep(0.5)
        self.assertTrue(self._verified)

    def tearDown(self):
        self._verified = False
