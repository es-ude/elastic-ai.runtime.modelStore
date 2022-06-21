from paho.mqtt import subscribe
import hashlib
import threading
from urllib.parse import urlparse
from service.client_connection import ClientConnection
from service.connection import Connection


class IllegalInput(Exception):
    pass


class RequestHandler:
    def __init__(self, service_commands):
        self._service_commands = service_commands

    def _get_input_from_message(self, message) -> tuple[int, str]:
        message_str = bytes.decode(message.payload)
        # messageStr = str(message)
        decoded_message = message_str.split("$")  # $=Trennzeichen
        if 2 != len(decoded_message):
            raise IllegalInput("Message must contain only node_id and model_uri sperated by '$'")

        return int(decoded_message[0]), decoded_message[1]

    def _on_message_get_model(self, client, _userdata, message):
        # todo: catch illegalInput Exception and send feedback to Elastic Node?
        decoded_message = self._get_input_from_message(message)
        node_id = decoded_message[0]
        model_uri = decoded_message[1]

        client = ClientConnection(node_id, self._service_commands)
        client_thread = threading.Thread(target=client.get_and_serve_model, args=(model_uri, ))
        client_thread.start()

    def wait_for_elastic_node(self):
        Connection().receive(self._on_message_get_model, "getModel")
