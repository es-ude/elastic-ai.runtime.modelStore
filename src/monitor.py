import service
import argparse

class Monitor:
	def __init__(self, model_store_uri, mqtt_broker):
		self._model_store_uri = model_store_uri
		self._mqtt_broker = mqtt_broker

	def run(self):
		store_connection = service.store_connection.MLflowStoreConnection(self._model_store_uri)
		print("initialized storeConnection")
		service_commands = service.service_commands.ServiceCommands(store_connection)
		print("initialized serviceCommands")
		request_handler = service.request_handler.RequestHandler(service_commands, self._mqtt_broker)
		print("initialized request handler")
		request_handler.wait_for_elastic_node()

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Monitor")
	parser.add_argument(
        "--store",
        type=str,
        default="http://localhost:5000",
        help="connect to the model Store on the given uri",
    )
	parser.add_argument(
        "--broker",
        type=str,
        default="broker.hivemq.com",
        help="mqtt broker to connect to",
    )
	args = parser.parse_args()

	monitor = Monitor(args.store, args.broker)
	monitor.run()
