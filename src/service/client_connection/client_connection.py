from paho.mqtt import publish

from service.store_connection import ModelNotFound


HOSTNAME = "broker.hivemq.com"
MODEL_NOT_FOUND_ERROR = b"1"  # gets send to the client, if the model could not be found


class ClientConnection:
    def __init__(self, node_id, service_commands):
        self._node_id = node_id
        self._service_commands = service_commands
        self._topic = "/" + str(self._node_id)

    def get_model(self, model_name: str):
        model = self._service_commands.get_model(model_name)
        return model.formats["tflite"]

    def serve_model(self, model: bytearray):
        publish.single(self._topic, payload=model, hostname=HOSTNAME)

    def _send_model_not_found(self):
        publish.single(self._topic, payload=MODEL_NOT_FOUND_ERROR, hostname=HOSTNAME)

    def get_and_serve_model(self, model_name: str):
        try:
            model = self.get_model(model_name)
            self.serve_model(model)
        except ModelNotFound:
            self._send_model_not_found()
