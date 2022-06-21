from service.store_connection import ModelNotFound


class MockModel:
    name = "hello_world"
    version = 1
    format = "tflite"
    data = 0

    def __init__(self):
        pass


class MockServiceCommands:
    def __init__(self):
        pass

    def get_model(self, model_uri):
        if model_uri == "model:6d6f636b": # 'mock'
            return MockModel()
        else:
            raise ModelNotFound
