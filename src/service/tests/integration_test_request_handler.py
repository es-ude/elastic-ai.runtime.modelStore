from cgitb import handler
import unittest
import _thread
import time
from service.request_handler import requestHandler
from service.mocks import mock_serviceCommands
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

NODE_ID = "15"
SEPERATOR = "$"

class integrationTest_requestHandler(unittest.TestCase):
    
    def setUp(self) -> None:
        self._handler = requestHandler(mock_serviceCommands())

    def _callback(self, client, userdata, message):
        self._arrived = True      
        self.assertEquals(message.payload, b'0')    #mock serviceCommands sends b'0' as model

    def _subscribe_helper(self):
        subscribe.callback(self._callback, "/"+NODE_ID, hostname="broker.hivemq.com")

    def test_subscribe(self):
        self._arrived = False
        _thread.start_new_thread(self._handler.waitForElasticNode, ())   #call the method that is beeing tested
        _thread.start_new_thread(self._subscribe_helper, ())            #Helper thread to subscribe
        time.sleep(0.5)

        #send a message for the request_handler to handle
        message = NODE_ID + SEPERATOR + "hello_world"
        publish.single("/service/getModel", payload=message, hostname="broker.hivemq.com")
        time.sleep(0.5) 
        
        self.assertTrue(self._arrived)

