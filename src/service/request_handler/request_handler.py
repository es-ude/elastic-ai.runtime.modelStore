from paho.mqtt import subscribe

from service.client_connection import ClientConnection


class IllegalInput(Exception):
    pass


class RequestHandler:
    def __init__(self, service_commands, mqtt_broker):
        self._service_commands = service_commands
        self._mqtt_broker = mqtt_broker

    def _get_input_from_message(self, message) -> tuple[int, str]:
        message_str = bytes.decode(message.payload)
        # messageStr = str(message)
        decoded_message = message_str.split("$")  # $=Trennzeichen
        if 2 != len(decoded_message):
            raise IllegalInput("Message must contain only NodeId and modelName sperated by '$'")
        return int(decoded_message[0]), decoded_message[1]

    def _on_message_get_model(self, client, _userdata, message):
        # todo: catch illegalInput Exception and send feedback to Elastic Node?
        decoded_message = self._get_input_from_message(message)
        node_id = decoded_message[0]
        model_name = decoded_message[1]

        client = ClientConnection(node_id, self._service_commands, self._mqtt_broker)
        client.get_and_serve_model(model_name)

    def wait_for_elastic_node(self):
        subscribe.callback(
            self._on_message_get_model, "/service/getModel", hostname="broker.hivemq.com"
        )
