import threading
import traceback

from service.application_layer_connection import ApplicationLayerConnection
from service.client_connection import ModelServer
from service.errors import IllegalInput


class RequestHandler:
    def __init__(self, service_commands):
        self._service_commands = service_commands

    def _decode_message(self, message: bytes) -> tuple[int, list[str]]:
        message_str = message.decode()
        decoded_message = message_str.split("$")  # $=Trennzeichen
        if len(decoded_message) < 2:
            raise IllegalInput(
                "Message should consist of the client ID and arguments, separated by '$'"
            )

        try:
            client_id = int(decoded_message[0])
        except ValueError as e:
            raise IllegalInput("Client ID should be an integer value") from e

        return client_id, decoded_message[1:]

    def _on_message_get_model(self, client, _userdata, message):
        try:
            client_id, arguments = self._decode_message(message.payload)

            client = ModelServer(client_id, self._service_commands)
            client_thread = threading.Thread(target=client.serve_model, args=(arguments, ))
            client_thread.start()
        except Exception:
            # can't send exception to client here since we don't know the right node id to send to
            print(f"Request handler exception while handling getModel request {message.payload}:")
            traceback.print_exc()

    def _on_message_search_model(self, client, _userdata, message):
        try:
            client_id, arguments = self._decode_message(message.payload)

            client = ModelServer(client_id, self._service_commands)
            client_thread = threading.Thread(target=client.search_for_model, args=(arguments, ))
            client_thread.start()
        except Exception:
            # can't send exception to client here since we don't know the right node id to send to
            print(f"Request handler exception while handling getModel request {message.payload}:")
            traceback.print_exc()

    def wait_for_elastic_node(self):
        connection = ApplicationLayerConnection()
        get_model_thread = threading.Thread(
            target=connection.receive,
            args=(self._on_message_get_model, "getModel", )
        )
        search_model_thread = threading.Thread(
            target=connection.receive,
            args=(self._on_message_search_model, "searchModel", )
        )

        get_model_thread.start()
        search_model_thread.start()
