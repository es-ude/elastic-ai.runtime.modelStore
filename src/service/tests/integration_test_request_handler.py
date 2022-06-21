import _thread
import time
import unittest

from paho.mqtt import publish, subscribe

from service.request_handler import RequestHandler
from service.mocks import MockServiceCommands


NODE_ID = "15"
SEPERATOR = "$"
PUBLIC_BROKER = "broker.hivemq.com"


class IntegrationTestRequestHandler(unittest.TestCase):
    def setUp(self) -> None:
        self._handler = RequestHandler(MockServiceCommands())
        self._arrived = False

    def _callback(self, _client, _userdata, message):
        self._arrived = True
        self.assertEqual(message.payload, b"0")  # mock serviceCommands sends b'0' as model

    def _subscribe_helper(self):
        subscribe.callback(self._callback, "/" + NODE_ID, hostname=PUBLIC_BROKER)

    def _call_wait_for_elastic_node(self):
        _thread.start_new_thread(self._handler.wait_for_elastic_node, ())

    def _subscribe_to_public_broker(self):
        _thread.start_new_thread(self._subscribe_helper, ())  # Helper thread to subscribe

    def _send_mqtt_request_for_model(self):
        message = NODE_ID + SEPERATOR + "model:6d6f636b" # 'mock'
        publish.single("/service/getModel", payload=message, hostname=PUBLIC_BROKER)
        time.sleep(1)

    def test_subscribe(self):
        self._call_wait_for_elastic_node()
        self._subscribe_to_public_broker()
        time.sleep(1)

        self._send_mqtt_request_for_model()

        self.assertTrue(self._arrived)
