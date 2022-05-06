import service
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

def getModelFromMessage(message)->str:
	messageStr=bytes.decode(message.payload)
	decodedMessage = messageStr.split("$") #$=Trennzeichen
	return decodedMessage[1]
	
def getNodeFromMessage(message)->int:
	messageStr=bytes.decode(message.payload)
	decodedMessage = messageStr.split("$") #$=Trennzeichen
	return decodedMessage[0]

def on_message_service(client, userdata, message):
	nodeId = getNodeFromMessage(message)
	wantedModel = getModelFromMessage(message)
	
	elastic_node = service.es_connection.esConnection(nodeId,serviceCommands)
	model = elastic_node.connectForSearch(wantedModel)
	elastic_node.serveModel(model)

def waitForElasticNode():
	subscribe.callback(on_message_service, "/service", hostname="broker.hivemq.com")

if __name__=="__main__": 
	storeConnection = service.store_connection.ExampleStoreConnection()
	#storeConnection = service.store_connection.MLflowStoreConnection()
	serviceCommands = service.service_commands.serviceCommands(storeConnection)
	waitForElasticNode()

