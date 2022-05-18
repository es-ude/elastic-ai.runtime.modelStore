from service.store_connection import ModelNotFound

class mockModel():
    files={"model.tflite":0}
    name="hello_world"
    def __init__(self):
        pass

class mock_serviceCommands():
    def __init__(self):
        pass
    def getModel(self, modelName):
        if modelName == "hello_world":
            return mockModel()
        else:
            raise ModelNotFound