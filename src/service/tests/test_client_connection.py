import unittest
from service.client_connection import clientConnection
from service.mocks import mock_serviceCommands
from service.store_connection import ModelNotFound

NODE_ID = 1

class test_clientConnection(unittest.TestCase):
    def setUp(self):
        self._serviceCommands = mock_serviceCommands()
        self._client = clientConnection(NODE_ID,self._serviceCommands)

    def test_constructorCall(self):
        client = clientConnection(NODE_ID, None)
        self.assertEqual(NODE_ID,client._nodeId)
        self.assertEqual(None, client._serviceCommands)

    def test_getModel(self):                             
        self.assertEqual(0, self._client.getModel("hello_world"))

    
    def test_getModel_modelNotFound(self):
        self.assertRaises(ModelNotFound, self._client.getModel, "wrong_model" )

    def tearDown(self):
        pass
