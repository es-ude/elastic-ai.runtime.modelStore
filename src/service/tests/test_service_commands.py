import unittest
from service.mocks import mock_storeConnection, mockModel
from service.service_commands import serviceCommands
from service.store_connection import ModelNotFound

MLFLOW_URI = "http://localhost:6000"

class test_serviceCommands(unittest.TestCase):
    def setUp(self):
        self._store = mock_storeConnection()
        self._serviceCommands = serviceCommands(self._store)

    def test_getModel(self):
        model1 = mockModel()
        model2 = self._serviceCommands.getModel(model1.name)
        self.assertEqual(model1.name, model2.name)
        self.assertEqual(model1.files, model2.files)
        
    def test_getModel_notString(self):
        self.assertRaises(TypeError, self._serviceCommands.getModel, 2)

    def test_getModel_modelNotFound(self):
        self.assertRaises(ModelNotFound, self._serviceCommands.getModel, "missing_model")