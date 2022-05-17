from service.mocks import mockModel
from service.store_connection import ModelNotFound

class mock_storeConnection():
    def getModel(self, modelName:str):
        if not isinstance(modelName, str):
            raise TypeError("modelName")
        
        if modelName == "hello_world":
            return mockModel()
        else:
            raise ModelNotFound