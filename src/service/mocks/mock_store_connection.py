from service.mocks import MockModel
from service.store_connection import ModelNotFound


class MockStoreConnection:
    def get_model(self, model_hash: bytes):
        if not isinstance(model_hash, bytes):
            raise TypeError("model_hash")

        if model_hash == b"mock":
            return MockModel()
        else:
            raise ModelNotFound
