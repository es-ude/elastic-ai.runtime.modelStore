import unittest

from service.client_connection import ClientConnection
from service.mocks import MockServiceCommands
from service.store_connection import ModelNotFound


NODE_ID = 1


class TestClientConnection(unittest.TestCase):
    def setUp(self):
        self._service_commands = MockServiceCommands()
        self._client = ClientConnection(NODE_ID, self._service_commands)

    # pylint: disable=protected-access
    def test_constructor_call(self):
        client = ClientConnection(NODE_ID, None)
        self.assertEqual(NODE_ID, client._node_id)
        self.assertEqual(None, client._service_commands)

    def test_get_model(self):
        self.assertEqual(0, self._client.get_model("hello_world"))

    def test_get_model_model_not_found(self):
        self.assertRaises(ModelNotFound, self._client.get_model, "wrong_model")

    def tearDown(self):
        pass
