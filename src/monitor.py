import service
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

if __name__=="__main__": 
	storeConnection = service.store_connection.ExampleStoreConnection()
	#storeConnection = service.store_connection.MLflowStoreConnection()
	serviceCommands = service.service_commands.serviceCommands(storeConnection)
	esManager = service.es_manager.esManager(serviceCommands)	
	esManager.waitForElasticNode()

