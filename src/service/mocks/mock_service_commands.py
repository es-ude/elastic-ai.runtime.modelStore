from service.store_connection import ModelNotFound


class MockModel:
    files = {"model.tflite": 0}
    name = "hello_world"

    def __init__(self):
        pass


class MockServiceCommands:
    def __init__(self):
        pass

    def get_model(self, model_name):
        if model_name == "hello_world":
            return MockModel()
        else:
            raise ModelNotFound
