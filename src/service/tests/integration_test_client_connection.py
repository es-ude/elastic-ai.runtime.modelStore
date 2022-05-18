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

    
    def _subscribe_helper(self):
        subscribe.callback(self._deliver, "/"+str(NODE_ID), hostname="broker.hivemq.com")

    def _deliver(self, client, userdata, message):
        self.assertEquals(message.payload, b'0')        #mock service commands sends b'0' as model
        self._veryfied = True
        _thread.exit()

    def _subscribeHelper_ModelNotFound(self):
        subscribe.callback(self._deliver_ModelNotFound, "/"+str(NODE_ID), hostname="broker.hivemq.com")

    def _deliver_ModelNotFound(self, client, userdata, message):
        self.assertEqual(message.payload, MODEL_NOT_FOUND_ERROR)
        self._veryfied = True
        _thread.exit()

    #Tests if a served model can be received
    def test_serveEmptyModel(self):

        #Subscribe to topic /1
        _thread.start_new_thread(self._subscribe_helper, ())
        time.sleep(0.5)                                       #Problem: Nach F.I.R.S.T Prinzip müssen Tests immer schnell sein.

        self._client.serveModel(self._model.files["model.tflite"])
        
        time.sleep(0.5)
        self.assertTrue(self._veryfied) 

        #tell the client, that the wanted model could not be found
    def test_ModelNotFound(self):
        _thread.start_new_thread(self._subscribeHelper_ModelNotFound, ())
        time.sleep(0.5)

        self._client.getAndServeModel("unknown_model")
        time.sleep(0.5)
        self.assertTrue(self._veryfied) 


    def tearDown(self):
        self._verified = False