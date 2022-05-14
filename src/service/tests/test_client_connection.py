import unittest
from service.client_connection import clientConnection
from service.mocks import mock_serviceCommands

NODE_ID = 1

class test_clientConnection(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructorCall(self):
        client = clientConnection(NODE_ID, None)
        self.assertEqual(NODE_ID,client._nodeId)
        self.assertEqual(None, client._serviceCommands)

    def test_getModel(self):                              #Unit Test hier sinnlos? Direkt nur als integration test?
        serviceCommands = mock_serviceCommands()
        client = clientConnection(NODE_ID,serviceCommands)
        self.assertEqual(0, client.getModel("model 1"))

    # serveModel() mit Unit Test nicht testbar?     


    def tearDown(self):
        pass
