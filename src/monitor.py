import service

if __name__=="__main__": 
	storeConnection = service.store_connection.MLflowStoreConnection("http://localhost:5000")
	print("initialized storeConnection")
	serviceCommands = service.service_commands.ServiceCommands(storeConnection)
	print("initialized serviceCommands")
	requestHandler = service.request_handler.RequestHandler(serviceCommands)	
	print("initialized request handler")
	requestHandler.wait_for_elastic_node()
