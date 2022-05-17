import unittest

from service.entities import Model
from service.store_connection.mlflow import MLflowStoreConnection, ModelNotFound


class BaseTest_MLflowStoreConnection(unittest.TestCase):
	def setUp(self):
		self.storeConnection = MLflowStoreConnection(self.mlflowUri)

	def test_getModel(self):
		model = self.storeConnection.getModel("valid_model")

		self.assertIsInstance(model, Model)
		self.assertEqual(model.name, "valid_model")
		self.assertEqual(model.version, 2)
		self.assertIn("tflite", model.formats)
		self.assertIn(model.formats["tflite"], model.files)

		self.assertEqual(model.files[model.formats["tflite"]], self.referenceModelData)

	def test_getModel_invalidModel(self):
		self.assertRaises(ModelNotFound, self.storeConnection.getModel, "invalid_model")

	def test_getModel_invalidName(self):
		for v in (None, 1234):
			with self.subTest(v):
				self.assertRaises(TypeError, self.storeConnection.getModel, v)

	def test_getNewestVersion(self):
		version = self.storeConnection.getNewestVersion("valid_model")
		self.assertIsInstance(version, int)
		self.assertEqual(version, 2)

	def test_getNewestVersion_invalidModel(self):
		self.assertRaises(ModelNotFound, self.storeConnection.getNewestVersion, "invalid_model")

	def test_getNewestVersion_invalidName(self):
		for v in (None, 1234):
			with self.subTest(v):
				self.assertRaises(TypeError, self.storeConnection.getNewestVersion, v)
