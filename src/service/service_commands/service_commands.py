from service.entities import Model
from service.store_connection import ModelNotFound


class ServiceCommands:
    def __init__(self, store_connection):
        self._store_connection = store_connection

    def get_model(self, model_name: str) -> Model:
        try:
            return self._store_connection.get_model(model_name)
        except TypeError as exc:
            raise exc
        except ModelNotFound as exc:
            raise exc
