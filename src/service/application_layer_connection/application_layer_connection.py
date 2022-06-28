from paho.mqtt import subscribe, publish

#todo: config file
HOSTNAME = "broker.hivemq.com"

class ApplicationLayerConnection:
    def __init__(self):
        pass

    def send(self, client_id, payload):
        topic = "/" + str(client_id)
        publish.single(topic, payload=payload, hostname=HOSTNAME)


    def receive(self, callback, function: str):
        topic = ""

        if function == "getModel":
            topic = "/service/getModel"
        elif function == "searchModel":
            topic = "/service/searchModel"

        subscribe.callback(
            callback, topic, hostname=HOSTNAME
        )
