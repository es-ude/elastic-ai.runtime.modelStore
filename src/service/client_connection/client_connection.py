import paho.mqtt.publish as publish

class clientConnection():
    def __init__(self, nodeId, serviceCommands):
        self._nodeId = nodeId
        self._serviceCommands = serviceCommands

    def getModel(self, modelName:str):
        model = self._serviceCommands.getModel(modelName)
        return model.files['model.flite']

    def serveModel(self, model:bytearray):
        topic = "/" + str(self._nodeId)
        publish.single(topic, payload=model, hostname="broker.hivemq.com")