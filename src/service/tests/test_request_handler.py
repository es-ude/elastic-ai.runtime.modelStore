import unittest

from service.request_handler import RequestHandler, IllegalInput
from service.mocks import MockServiceCommands, MockMessage


# pylint: disable=protected-access
class TestRequestHandler(unittest.TestCase):
    def setUp(self) -> None:
        self._handler = RequestHandler(MockServiceCommands())

    def test_get_node_from_message(self):
        message_str = "55$some model"
        message = MockMessage(message_str)
        self.assertEqual(55, self._handler._get_input_from_message(message)[0])

    def test_get_model_from_message(self):
        message_str = "55$some model"
        message = MockMessage(message_str)
        self.assertEqual("some model", self._handler._get_input_from_message(message)[1])

    def test_get_with_short_input(self):
        message_str = "55somemodel"
        message = MockMessage(message_str)
        self.assertRaises(IllegalInput, self._handler._get_input_from_message, message)

    def test_get_with_long_input(self):
        message_str = "55$seomeModel$anotherModel"
        message = MockMessage(message_str)
        self.assertRaises(IllegalInput, self._handler._get_input_from_message, message)
