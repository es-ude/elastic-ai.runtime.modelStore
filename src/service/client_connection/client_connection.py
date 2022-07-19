import time
import traceback

from service.application_layer_connection import ApplicationLayerConnection
from service.errors import ErrorCode, IllegalInput, ModelStoreError


class ModelServer:
    def __init__(self, client_id, service_commands):
        self._client_id = client_id
        self._service_commands = service_commands
        self._connection = ApplicationLayerConnection()

    def _send_error(self, error_code: ErrorCode):
        # prefix all error messages with '!'
        self._connection.send(self._client_id, ("!" + str(int(error_code))).encode())

    def _decode_get_model(self, arguments: list[str]) -> str:
        if len(arguments) != 1:
            raise IllegalInput("getModel request should have 1 argument: model_id")

        return arguments[0]

    def _decode_search_model(self, arguments: list[str]) -> str:
        if len(arguments) != 1:
            raise IllegalInput("searchModel request should have 1 argument: problem_graph")

        return arguments[0]

    def _get_model(self, model_uri: str):
        model = self._service_commands.get_model(model_uri)
        return model.data_url

    def serve(self, model_data_url: str):
        self._connection.send(self._client_id, model_data_url.encode())

    def serve_model(self, arguments: list[str]):
        try:
            model_uri = self._decode_get_model(arguments)
            model_data_url = self._get_model(model_uri)
            self.serve(model_data_url)
        except ModelStoreError as e:
            self._send_error(e.error_code)
        except Exception:
            self._send_error(ErrorCode.OTHER)
            print(
                f"Exception while handling getModel request from {self._client_id}, arguments {arguments}:"
            )
            traceback.print_exc()

    def search_for_model(self, arguments: list[str]):
        try:
            problem_graph = self._decode_search_model(arguments)
            model_uri = self._service_commands.search_model(problem_graph)
            time.sleep(0.5)
            self.serve(model_uri)
        except ModelStoreError as e:
            self._send_error(e.error_code)
        except Exception:
            self._send_error(ErrorCode.OTHER)
            print(
                f"Exception while handling searchModel request from {self._client_id}, arguments {arguments}:"
            )
            traceback.print_exc()
