import unittest
import service
#from service.tests import test_clientConnection



loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_request_handler))
suite.addTests(loader.loadTestsFromModule(service.tests.test_client_connection))
suite.addTests(loader.loadTestsFromModule(service.tests.integration_test_client_connection))
suite.addTests(loader.loadTestsFromModule(service.tests.test_request_handler))


runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
