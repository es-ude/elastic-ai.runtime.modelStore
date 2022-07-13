import unittest

from service.errors import ModelDataNotFound
from service.mocks import MockModel, MockModelUriFinder, MockStoreConnection
from service.service_commands import ServiceCommands


MLFLOW_URI = "http://localhost:6000"


class TestServiceCommands(unittest.TestCase):
    def setUp(self):
        self._store = MockStoreConnection()
        self._model_uri_finder = MockModelUriFinder()
        self._service_commands = ServiceCommands(self._store, self._model_uri_finder)

    def test_get_model(self):
        model1 = MockModel()
        model2 = self._service_commands.get_model("model:6d6f636b")  # 'mock'
        self.assertEqual(model1.name, model2.name)
        self.assertEqual(model1.version, model2.version)
        self.assertEqual(model1.format, model2.format)
        self.assertEqual(model1.data_url, model2.data_url)

    def test_get_model_not_string(self):
        self.assertRaises(TypeError, self._service_commands.get_model, 2)

    def test_get_model_model_not_found(self):
        self.assertRaises(
            ModelDataNotFound, self._service_commands.get_model, "model:696e76616c6964"
        )  # 'invalid'
