import unittest

import service


loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(service.tests.test_client_connection))
suite.addTests(loader.loadTestsFromModule(service.tests.test_request_handler))
suite.addTests(loader.loadTestsFromModule(service.tests.test_service_commands))
suite.addTests(loader.loadTestsFromModule(service.tests.test_mlflow_store_connection))


runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
