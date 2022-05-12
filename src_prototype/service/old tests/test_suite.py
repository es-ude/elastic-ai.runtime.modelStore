import unittest

import test_modelBuffer

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_modelBuffer))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)