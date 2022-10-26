import sys
import unittest

import service

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_client_connection))
suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_request_handler))
suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_mlflow_store_connection))
suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_model_finder))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
sys.exit(not result.wasSuccessful())
