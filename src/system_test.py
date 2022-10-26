import sys
import unittest

import service

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(service.tests.system_test_search_model))
suite.addTests(loader.loadTestsFromModule(service.tests.system_test_get_model))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
sys.exit(not result.wasSuccessful())
