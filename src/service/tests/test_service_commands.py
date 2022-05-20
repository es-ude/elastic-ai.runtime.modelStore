import unittest

from service.mocks import MockStoreConnection, MockModel
from service.service_commands import ServiceCommands
from service.store_connection import ModelNotFound


MLFLOW_URI = "http://localhost:6000"


class TestServiceCommands(unittest.TestCase):
    def setUp(self):
        self._store = MockStoreConnection()
        self._service_commands = ServiceCommands(self._store)

    def test_get_model(self):
        model1 = MockModel()
        model2 = self._service_commands.get_model(model1.name)
        self.assertEqual(model1.name, model2.name)
        self.assertEqual(model1.files, model2.files)

    def test_get_model_not_string(self):
        self.assertRaises(TypeError, self._service_commands.get_model, 2)

    def test_get_model_model_not_found(self):
        self.assertRaises(ModelNotFound, self._service_commands.get_model, "missing_model")
