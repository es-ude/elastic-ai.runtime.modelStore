from platform import node
from service.store_connection import ModelNotFound
from service.connection import Connection


MODEL_NOT_FOUND_ERROR = b"1"  # gets send to the client, if the model could not be found


class ClientConnection:
    def __init__(self, node_id, service_commands):
        self._node_id = node_id
        self._service_commands = service_commands
        self._connection = Connection()

    def get_model(self, model_uri: str):
        model = self._service_commands.get_model(model_uri)
        return model.data_url

    def serve_model(self, model_data_url: str):
        self._connection.send(self._node_id, model_data_url)

    def _send_model_not_found(self):
        self._connection.send(self._node_id, MODEL_NOT_FOUND_ERROR)

    def get_and_serve_model(self, model_uri: str):
        try:
            model_data_url = self.get_model(model_uri)
            self.serve_model(model_data_url)
        except ModelNotFound:
            self._send_model_not_found()

''''
class ClientConnection:
    def __init__(self, node_id, service_commands, hostname):
        ...


def client_connection_factory(hostname):
    def create_client_connection(node_id, service_commands):
        return ClientConnection(node_id, service_commands, hostname)
    return create_client_connection

from functools import partial

HiveMQClientConnection = partial(ClientConnection, hostname="broker.hivemq.com")
'''
