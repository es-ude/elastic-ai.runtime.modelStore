import unittest

from service.entities import Model
from service.store_connection.mlflow import MLflowStoreConnection, ModelNotFound


class BaseTestMLflowStoreConnection(unittest.TestCase):
    mlflow_uri = None
    reference_model_data = None

    def setUp(self):
        self.store_connection = MLflowStoreConnection(self.mlflow_uri)

    def test_get_existing_model(self):
        model = self.store_connection.get_model("valid_model")

        self.assertIsInstance(model, Model)
        self.assertEqual(model.name, "valid_model")
        self.assertEqual(model.version, 2)
        self.assertIn("tflite", model.formats)

        self.assertEqual(model.formats["tflite"], self.reference_model_data)

    def test_get_nonexistent_model(self):
        self.assertRaises(ModelNotFound, self.store_connection.get_model, "invalid_model")

    def test_get_model_with_invalid_name(self):
        for invalid_name in (None, 1234):
            with self.subTest(invalid_name):
                self.assertRaises(TypeError, self.store_connection.get_model, invalid_name)

    def test_get_newest_version_of_existing_model(self):
        version = self.store_connection.get_newest_version("valid_model")
        self.assertIsInstance(version, int)
        self.assertEqual(version, 2)

    def test_get_newest_version_of_nonexistent_model(self):
        self.assertRaises(ModelNotFound, self.store_connection.get_newest_version, "invalid_model")

    def test_get_newest_version_with_invalid_name(self):
        for invalid_name in (None, 1234):
            with self.subTest(invalid_name):
                self.assertRaises(TypeError, self.store_connection.get_newest_version, invalid_name)
