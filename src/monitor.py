import service
import argparse

class Monitor:
	def __init__(self,  model_store_uri):
		self._model_store_uri = model_store_uri

	def run(self):
		store_connection = service.store_connection.MLflowStoreConnection(self._model_store_uri)
		print("initialized storeConnection")
		service_commands = service.service_commands.ServiceCommands(store_connection)
		print("initialized serviceCommands")
		request_handler = service.request_handler.RequestHandler(service_commands)
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
	args = parser.parse_args()

	monitor = Monitor(args.store)
	monitor.run()
