import unittest
from service.request_handler import requestHandler, illegalInput
from service.mocks import mock_serviceCommands, mockMessage

class test_requestHandler(unittest.TestCase):
    def setUp(self) -> None:
        self._handler = requestHandler(mock_serviceCommands())

    def test_getNodeFromMessage(self):
        messageStr = "55$some model"
        message = mockMessage(messageStr)
        self.assertEqual(55, self._handler._getInputFromMessage(message)[0])

    def test_getModelFromMessage(self):
        messageStr = "55$some model"
        message = mockMessage(messageStr)
        self.assertEqual("some model", self._handler._getInputFromMessage(message)[1])

    def test_getWithShortInput(self):
        messageStr = "55somemodel"
        message = mockMessage(messageStr)
        self.assertRaises(illegalInput, self._handler._getInputFromMessage, message)

    def test_getWithLongInput(self):
        messageStr = "55$seomeModel$anotherModel"
        message = mockMessage(messageStr)
        self.assertRaises(illegalInput, self._handler._getInputFromMessage, message)