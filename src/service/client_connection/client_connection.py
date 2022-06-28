from platform import node
from service.store_connection import ModelNotFound
from service.application_layer_connection import ApplicationLayerConnection


MODEL_NOT_FOUND_ERROR = b"1"  # gets send to the client, if the model could not be found


class ModelServer:
    def __init__(self, client_id, service_commands):
        self._client_id = client_id
        self._service_commands = service_commands
        self._connection = ApplicationLayerConnection()

    def get_model(self, model_uri: str):
        model = self._service_commands.get_model(model_uri)
        return model.data_url

    def serve(self, model_data_url: str):
        self._connection.send(self._client_id, model_data_url)

    def _send_model_not_found(self):
        self._connection.send(self._client_id, MODEL_NOT_FOUND_ERROR)

    def serve_model(self, model_uri: str):
        try:
            model_data_url = self.get_model(model_uri)
            self.serve(model_data_url)
        except ModelNotFound:
            self._send_model_not_found()

    def search_for_model(self, problem_graph):
        try:
            model_uri = self._service_commands.search_model(problem_graph)
            self.serve(model_uri)
        except ModelNotFound:
            self._send_model_not_found()    #is it better to use a different exception?

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
