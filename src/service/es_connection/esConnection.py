import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from fake_serviceCommands import fake_serviceCommands

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
	
	elastic_node = esConnection(nodeId)
	model = elastic_node.connectForSearch(wantedModel)
	elastic_node.serveModel(model)

def waitForElasticNode():
	subscribe.callback(on_message_service, "/service", hostname="broker.hivemq.com")


class esConnection():
	_nodeId=1 #Node braucht eine eindeutige id
	 
	def __init__(self, nodeId):	
		self._nodeId = nodeId
	
	def connectForSearch(self, modelName:str)->str:		#todo:bytes statt string
		commands = fake_serviceCommands()
		model = commands.search(modelName)
		return model
		
	def serveModel(self, model:str):	
		topic = "/"+str(self._nodeId)
		publish.single(topic, payload=model, hostname="broker.hivemq.com")

if __name__=="__main__":
	waitForElasticNode()
