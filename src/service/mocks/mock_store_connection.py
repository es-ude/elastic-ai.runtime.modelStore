from service.errors import ModelDataNotFound
from service.mocks import MockModel


class MockStoreConnection:
    def get_model(self, model_hash: bytes):
        if not isinstance(model_hash, bytes):
            raise TypeError("model_hash")

        if model_hash == b"mock":
            return MockModel()
        else:
            raise ModelDataNotFound
