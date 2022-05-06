from service.es_connection import esConnection
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

class esManager:
	def __init__(self, serviceCommands):
		self._serviceCommands = serviceCommands
		
	def _getModelFromMessage(self, message)->str:
		messageStr=bytes.decode(message.payload)
		decodedMessage = messageStr.split("$") #$=Trennzeichen
		return decodedMessage[1]
	
	def _getNodeFromMessage(self, message)->int:
		messageStr=bytes.decode(message.payload)
		decodedMessage = messageStr.split("$") #$=Trennzeichen
		return decodedMessage[0]

	def _on_message_service(self, client, userdata, message):
		nodeId = self._getNodeFromMessage(message)
		wantedModel = self._getModelFromMessage(message)
	
		elastic_node = esConnection(nodeId,self._serviceCommands)
		model = elastic_node.connectForSearch(wantedModel)
		elastic_node.serveModel(model)
		
	def waitForElasticNode(self):
		subscribe.callback(self._on_message_service, "/service", hostname="broker.hivemq.com")

		
