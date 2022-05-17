from service.entities import Model
from service.store_connection import ModelNotFound

class serviceCommands():
    def __init__(self, storeConnection):
        self._storeConnection = storeConnection

    def getModel(self, modelName:str)->Model:
        try:
            return self._storeConnection.getModel(modelName)
        except TypeError as e:
            raise e
        except ModelNotFound as e:
            raise e
