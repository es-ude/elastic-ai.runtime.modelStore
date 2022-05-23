import service
import argparse

class Monitor:
	def __init__(self, model_store_uri):
		self._model_store_uri = model_store_uri

	def run(self):
		storeConnection = service.store_connection.MLflowStoreConnection("http://localhost:5000")
		print("initialized storeConnection")
		serviceCommands = service.service_commands.ServiceCommands(storeConnection)
		print("initialized serviceCommands")
		requestHandler = service.request_handler.RequestHandler(serviceCommands)
		print("initialized request handler")
		requestHandler.wait_for_elastic_node()

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
