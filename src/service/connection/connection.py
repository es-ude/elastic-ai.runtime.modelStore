from paho.mqtt import subscribe, publish

#todo: config file
HOSTNAME = "broker.hivemq.com"

class Connection:
    def __init__(self):
        pass

    def send(self, node_id, payload):
        topic = "/" + str(node_id)
        publish.single(topic, payload=payload, hostname=HOSTNAME)


    def receive(self, callback, function: str):
        topic = ""

        if function == "getModel":
            topic = "/service/getModel"

        subscribe.callback(
            callback, topic, hostname=HOSTNAME
        )
