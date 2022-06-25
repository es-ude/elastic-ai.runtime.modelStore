import unittest

from service.request_handler import RequestHandler, IllegalInput
from service.mocks import MockServiceCommands


PUBLIC_BROKER = "broker.hivemq.com"

# pylint: disable=protected-access
class TestRequestHandler(unittest.TestCase):
    def setUp(self) -> None:
        self._handler = RequestHandler(MockServiceCommands())

    def test_get_node_from_message(self):
        message_str = "55$some model"
        message = message_str.encode()
        self.assertEqual(55, self._handler._decode_message(message)[0])

    def test_get_arguments_from_message(self):
        message_str = "55$some model"
        message = message_str.encode()
        self.assertEqual(["some model"], self._handler._decode_message(message)[1])

    def test_get_with_short_input(self):
        message_str = "55somemodel"
        message = message_str.encode()
        self.assertRaises(IllegalInput, self._handler._decode_message, message)
