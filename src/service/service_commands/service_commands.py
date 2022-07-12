from urllib.parse import urlparse

from service.entities import Model
from service.errors import IllegalInput


class ServiceCommands:
    def __init__(self, store_connection, model_finder):
        self._store_connection = store_connection
        self._model_finder = model_finder

    def _parse_model_uri(self, model_uri: str) -> bytes:
        if not isinstance(model_uri, str):
            raise TypeError("model_uri")

        parsed_uri = urlparse(model_uri)
        if parsed_uri.scheme != "model":
            raise IllegalInput(f"Invalid model_uri '{model_uri}', expected scheme 'model:'")
        try:
            model_hash = bytes.fromhex(parsed_uri.path)
            return model_hash
        except ValueError as e:
            raise IllegalInput(f"Invalid model_uri '{model_uri}', invalid model hash") from e

    def get_model(self, model_uri: str) -> Model:
        model_hash = self._parse_model_uri(model_uri)
        return self._store_connection.get_model(model_hash)

    def search_model(self, problem_graph):
        store_graphs = self._store_connection.get_all_graphs()
        self._model_finder.load_json_graphs(store_graphs)
        model_uri = self._model_finder.search_for_model(problem_graph)
        return model_uri
