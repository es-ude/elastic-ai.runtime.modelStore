import unittest
from service.client_connection import clientConnection
from service.mocks import mock_serviceCommands

class test_clientConnection(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructorCall(self):
        client = clientConnection(1, None)
        self.assertEqual(1,client._nodeId)
        self.assertEqual(None, client._serviceCommands)

    def test_getModel(self):                              #Unit Test hier sinnlos? Direkt nur als integration test?
        serviceCommands = mock_serviceCommands()
        client = clientConnection(1,serviceCommands)
        self.assertEqual(None, client.getModel("model 1"))

    # serveModel() mit Unit Test nicht testbar?     


    def tearDown(self):
        pass
