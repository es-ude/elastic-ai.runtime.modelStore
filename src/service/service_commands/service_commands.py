from urllib.parse import urlparse

from service.entities import Model


class ServiceCommands:
    def __init__(self, store_connection):
        self._store_connection = store_connection

    def _parse_model_uri(self, model_uri: str) -> bytes:
        if not isinstance(model_uri, str):
            raise TypeError("model_uri")

        parsed_uri = urlparse(model_uri)
        if parsed_uri.scheme != "model":
            raise ValueError(f"Invalid model_uri '{model_uri}', expected scheme 'model:'")
        try:
            model_hash = bytes.fromhex(parsed_uri.path)
            return model_hash
        except ValueError:
            raise ValueError(f"Invalid model_uri '{model_uri}', invalid model hash")

    def get_model(self, model_uri: str) -> Model:
        model_hash = self._parse_model_uri(model_uri)
        return self._store_connection.get_model(model_hash)
