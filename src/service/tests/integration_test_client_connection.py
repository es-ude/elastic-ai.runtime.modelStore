import unittest
from service.client_connection import clientConnection
from service.mocks import mock_serviceCommands, mockModel
import paho.mqtt.subscribe as subscribe
import _thread
import time

NODE_ID = 1
MODEL_NOT_FOUND_ERROR = b'1'

class IntegrationTest_clientConnection(unittest.TestCase):
    def setUp(self) -> None:
        self._serviceCommands = mock_serviceCommands()
        self._client = clientConnection(NODE_ID,self._serviceCommands)
        self._model = mockModel()
        self._veryfied = False

    def _subscribe_to_public_broker(self, callback):
        subscribe.callback(callback, "/"+str(NODE_ID), hostname="broker.hivemq.com")
    
    def _deliver(self, client, userdata, message):
        self.assertEquals(message.payload, b'0')        #mock service commands sends b'0' as model
        self._veryfied = True
        _thread.exit()

    def _deliver_ModelNotFound(self, client, userdata, message):
        self.assertEqual(message.payload, MODEL_NOT_FOUND_ERROR)
        self._veryfied = True
        _thread.exit()

    def _start_client_with_callback(self, callback):
        _thread.start_new_thread(self._subscribe_to_public_broker, (callback,))

    #Tests if a served model can be received
    def test_serveEmptyModel(self):

        #Subscribe to topic /1
        self._start_client_with_callback(self._deliver)
        time.sleep(0.5)                                      

        self._client.serveModel(self._model.files["model.flite"])
        
        time.sleep(0.5)
        self.assertTrue(self._veryfied) 

    def test_client_receives_error_after_requesting_unknown_model(self):
        self._start_client_with_callback(self._deliver_ModelNotFound)
        time.sleep(0.5)

        self._client.getAndServeModel("unknown_model")
        time.sleep(0.5)
        self.assertTrue(self._veryfied) 


    def tearDown(self):
        self._verified = False