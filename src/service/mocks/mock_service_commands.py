from service.errors import ModelNotFound


class MockModel:
    name = "hello_world"
    version = 1
    format = "tflite"
    data_url = "http://example.com/model/model.tflite"

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
