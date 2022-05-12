import service

if __name__=="__main__": 
	#storeConnection = service.store_connection.ExampleStoreConnection()
	storeConnection = service.store_connection.MLflowStoreConnection()
	print("initialized storeConnection")
	serviceCommands = service.service_commands.serviceCommands(storeConnection)
	print("initialized serviceCommands")
	esManager = service.es_manager.esManager(serviceCommands)	
	print("initialized esManager")
	esManager.waitForElasticNode()

