import unittest

from service.entities import Model
from service.store_connection.mlflow import MLflowStoreConnection, ModelNotFound


class BaseTestMLflowStoreConnection(unittest.TestCase):
    mlflow_uri = None
    reference_model_data = None
    reference_model_hash = None

    def setUp(self):
        self.store_connection = MLflowStoreConnection(self.mlflow_uri)

    def test_get_existing_model(self):
        model = self.store_connection.get_model(self.reference_model_hash)

        self.assertIsInstance(model, Model)
        self.assertEqual(model.name, "valid_model")
        self.assertEqual(model.version, 1)
        self.assertEqual(model.format, "tflite")
        self.assertEqual(model.data, self.reference_model_data)

    def test_get_nonexistent_model(self):
        self.assertRaises(ModelNotFound, self.store_connection.get_model, b"invalid hash".ljust(32, b"-"))

    def test_get_model_with_invalid_hash(self):
        for invalid_hash in (None, 1234):
            with self.subTest(invalid_hash):
                self.assertRaises(TypeError, self.store_connection.get_model, invalid_hash)

        with self.subTest(b"too short"):
            self.assertRaises(ValueError, self.store_connection.get_model, b"too short")
