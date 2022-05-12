import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
from .fake_serviceCommands import fake_serviceCommands

class esConnection():
	_nodeId=1 #Node braucht eine eindeutige id
	 
	def __init__(self, nodeId, serviceCommands):	
		self._nodeId = nodeId
		self._serviceCommands = serviceCommands
	
	def connectForSearch(self, modelName:str)->str:		#todo:bytes statt string
		#commands = fake_serviceCommands()
		model = self._serviceCommands.search(modelName)
		return model.files['model.tflite']
		
	def serveModel(self, model:str):	
		topic = "/"+str(self._nodeId)
		publish.single(topic, payload=model, hostname="broker.hivemq.com")
