import unittest
from service.client_connection import clientConnection
from service.mocks import mock_serviceCommands, mockModel
import paho.mqtt.subscribe as subscribe
import _thread
import time

NODE_ID = 1

class IntegrationTest_clientConnection(unittest.TestCase):
    def setUp(self) -> None:
        serviceCommands = mock_serviceCommands()
        self._client = clientConnection(NODE_ID,serviceCommands)
        self._model = mockModel()
    
    def _subscribe_helper(self):
        subscribe.callback(self.deliver, "/"+str(NODE_ID), hostname="broker.hivemq.com")

    def deliver(self, client, userdata, message):
        self.assertEquals(message.payload, b'0')        #mock service commands sends b'0' as model
        self._veryfied = True

    #Tests if a served model can be received
    def test_serveEmptyModel(self):
        self._veryfied = False

        #Subscribe to topic /1
        _thread.start_new_thread(self._subscribe_helper, ())
        time.sleep(0.5)                                       #Problem: Nach F.I.R.S.T Prinzip müssen Tests immer schnell sein.

        self._client.serveModel(self._model.files["model.flite"])
        
        time.sleep(0.5)
        self.assertTrue(self._veryfied) 