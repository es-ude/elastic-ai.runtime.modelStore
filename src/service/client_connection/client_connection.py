import paho.mqtt.publish as publish
from service.store_connection import ModelNotFound

HOSTNAME = "broker.hivemq.com"
MODEL_NOT_FOUND_ERROR = b'1'    #gets send to the client, if the model could not be found

class clientConnection():
    def __init__(self, nodeId, serviceCommands):
        self._nodeId = nodeId
        self._serviceCommands = serviceCommands
        self._topic = "/" + str(self._nodeId)

    def getModel(self, modelName:str):
        model = self._serviceCommands.getModel(modelName)
        return model.files['model.flite']

    def serveModel(self, model:bytearray):
        publish.single(self._topic, payload=model, hostname=HOSTNAME)

    def _sendModelNotFound(self):
        publish.single(self._topic, payload=MODEL_NOT_FOUND_ERROR, hostname=HOSTNAME)

    def getAndServeModel(self, modelName:str):
        try:
            model = self.getModel(modelName)
            self.serveModel(model)
        except ModelNotFound:
            self._sendModelNotFound()  