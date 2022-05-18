from base64 import decode
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from service.client_connection import clientConnection

class illegalInput(Exception):
	pass

class requestHandler:
    def __init__(self, serviceCommands):
        self._serviceCommands = serviceCommands

    def _getInputFromMessage(self, message)->tuple[int,str]:
        messageStr=bytes.decode(message.payload)
        #messageStr = str(message)
        decodedMessage = messageStr.split("$") #$=Trennzeichen
        if 2 != len(decodedMessage):
            raise illegalInput("Message must contain only NodeId and modelName sperated by '$'")        
        return (int(decodedMessage[0]), decodedMessage[1])

    def _on_message_getModel(self, client, userdata, message):     #todo: catch illegalInput Exception and send feedback to Elastic Node? 
        decodedMessage = self._getInputFromMessage(message)
        nodeId = decodedMessage[0]
        modelName = decodedMessage[1]

        client = clientConnection(nodeId, self._serviceCommands)
        client.getAndServeModel(modelName)
        
    def waitForElasticNode(self):
        subscribe.callback(self._on_message_getModel, "/service/getModel", hostname="broker.hivemq.com")

