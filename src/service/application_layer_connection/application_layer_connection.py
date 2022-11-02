import configparser

from paho.mqtt import publish, subscribe


class ApplicationLayerConnection:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read("configfile.ini")
        self._hostname = self._config["DEFAULT"]["Hostname"]

    def send(self, client_id, payload: bytes):
        topic = "/" + str(client_id)

        publish.single(topic, payload=payload, hostname=self._hostname)

    def receive(self, callback, function: str):
        topic = ""

        if function == "getModel":
            topic = "eip://uni-due.de/es/enV5/service/getModel"
        elif function == "searchModel":
            topic = "eip://uni-due.de/es/enV5/service/searchModel"

        subscribe.callback(callback, topic, hostname=self._hostname)
