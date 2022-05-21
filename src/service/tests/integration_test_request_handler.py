import _thread
import time
import unittest

from paho.mqtt import publish, subscribe

from service.request_handler import RequestHandler
from service.mocks import MockServiceCommands


NODE_ID = "15"
SEPERATOR = "$"


class IntegrationTestRequestHandler(unittest.TestCase):
    def setUp(self) -> None:
        self._handler = RequestHandler(MockServiceCommands())
        self._arrived = False

    def _callback(self, _client, _userdata, message):
        self._arrived = True
        self.assertEqual(message.payload, b"0")  # mock serviceCommands sends b'0' as model

    def _subscribe_helper(self):
        subscribe.callback(self._callback, "/" + NODE_ID, hostname="broker.hivemq.com")

    def test_subscribe(self):
        # call the method that is beeing tested
        _thread.start_new_thread(self._handler.wait_for_elastic_node, ())
        _thread.start_new_thread(self._subscribe_helper, ())  # Helper thread to subscribe
        time.sleep(0.5)

        # send a message for the request_handler to handle
        message = NODE_ID + SEPERATOR + "hello_world"
        publish.single("/service/getModel", payload=message, hostname="broker.hivemq.com")
        time.sleep(0.5)

        self.assertTrue(self._arrived)
