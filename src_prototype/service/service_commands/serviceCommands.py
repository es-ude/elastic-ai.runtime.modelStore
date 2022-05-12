from ..store_connection import example_store_connection
from service.entities import Model

class serviceCommands():
	def __init__(self, storeConnection):
		self._storeConnection = storeConnection
		
	def search(self, modelName:str)->Model:
		return self._storeConnection.getModel(modelName)
