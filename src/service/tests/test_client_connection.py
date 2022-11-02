import unittest

from service.client_connection import ModelServer
from service.errors import ModelDataNotFound
from service.mocks import MockServiceCommands

CLIENT_ID = 1
PUBLIC_BROKER = "broker.hivemq.com"


class TestModelServer(unittest.TestCase):
    def setUp(self):
        self._service_commands = MockServiceCommands()
        self._client = ModelServer(CLIENT_ID, self._service_commands)

    # pylint: disable=protected-access
    def test_constructor_call(self):
        client = ModelServer(CLIENT_ID, None)
        self.assertEqual(CLIENT_ID, client._client_id)
        self.assertEqual(None, client._service_commands)

    def test_get_model(self):
        self.assertEqual(
            "http://example.com/model/model.tflite", self._client._get_model("model:6d6f636b")
        )  # 'mock'

    def test_get_model_model_not_found(self):
        self.assertRaises(
            ModelDataNotFound, self._client._get_model, "model:696e76616c6964"
        )  # 'invalid'

    def tearDown(self):
        pass
