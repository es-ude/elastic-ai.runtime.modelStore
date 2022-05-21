import service

if __name__=="__main__": 
	storeConnection = service.store_connection.MLflowStoreConnection("http://localhost:5000")
	print("initialized storeConnection")
	serviceCommands = service.service_commands.serviceCommands(storeConnection)
	print("initialized serviceCommands")
	requestHandler = service.request_handler.requestHandler(serviceCommands)	
	print("initialized request handler")
	requestHandler.waitForElasticNode()

