import _thread
import time
import unittest

from paho.mqtt import subscribe

from service.client_connection import ModelServer
from service.errors import ErrorCode
from service.mocks import MockModel, MockServiceCommands


CLIENT_ID = 1
HOSTNAME = "broker.hivemq.com"


class IntegrationTestModelServer(unittest.TestCase):
    def setUp(self) -> None:
        self._service_commands = MockServiceCommands()
        self._client = ModelServer(CLIENT_ID, self._service_commands)
        self._model = MockModel()
        self._verified = False

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(callback, "/" + str(CLIENT_ID), hostname=HOSTNAME)

    def _deliver(self, _client, _userdata, message):
        self.assertEqual(message.payload, b"http://example.com/model/model.tflite")
        self._verified = True
        _thread.exit()

    def _deliver_model_not_found(self, _client, _userdata, message):
        self.assertEqual(
            message.payload, ("!" + str(int(ErrorCode.MODEL_DATA_NOT_FOUND))).encode()
        )
        self._verified = True
        _thread.exit()

    def _start_client_with_callback(self, callback):
        # return threading.Thread(target=self._subscribe_to_public_broker, args=(callback,))
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    # Tests if a served model can be received
    def test_serve_empty_model(self):
        self._start_client_with_callback(self._deliver)
        # clientThread.start()
        time.sleep(2)

        self._client.serve(self._model.data_url)

    def test_client_receives_error_after_requesting_unknown_model(self):
        self._start_client_with_callback(self._deliver_model_not_found)
        time.sleep(2)

        self._client.serve_model(
            # b"invalid hash".ljust(32, b"-")
            ["model:696e76616c696420686173682d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d"]
        )
        time.sleep(2)
        self.assertTrue(self._verified)

    def tearDown(self):
        self._verified = False
