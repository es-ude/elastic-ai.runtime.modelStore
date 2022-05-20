from service.mocks import MockModel
from service.store_connection import ModelNotFound


class MockStoreConnection:
    def get_model(self, model_name: str):
        if not isinstance(model_name, str):
            raise TypeError("modelName")

        if model_name == "hello_world":
            return MockModel()
        else:
            raise ModelNotFound
