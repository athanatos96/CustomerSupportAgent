# app/unittest/test_data_validate.py


import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.data_validation.data_validation import validate_and_extract


class TestValidateAndExtract(unittest.TestCase):

    def test_order_number_valid(self):
        valid, value = validate_and_extract("order_number", "ORD12345")
        self.assertTrue(valid)
        self.assertEqual(value, "ORD12345")

        valid, value = validate_and_extract("order_number", "ord67890")
        self.assertTrue(valid)
        self.assertEqual(value, "ORD67890")

    def test_order_number_invalid(self):
        invalid_cases = ["12345", "order123", "ordabc", "ord 12345", ""]
        for case in invalid_cases:
            valid, value = validate_and_extract("order_number", case)
            self.assertFalse(valid)
            self.assertIsNone(value)

    def test_category_en_valid(self):
        for input_val, expected in {
            "shipping": "shipping",
            "billing": "billing",
            "product": "product"
        }.items():
            valid, value = validate_and_extract("category", input_val, lang="en")
            self.assertTrue(valid)
            self.assertEqual(value, expected)

    def test_category_es_valid(self):
        for input_val, expected in {
            "envío": "shipping",
            "facturación": "billing",
            "producto": "product"
        }.items():
            valid, value = validate_and_extract("category", input_val, lang="es")
            self.assertTrue(valid)
            self.assertEqual(value, expected)

    def test_category_invalid(self):
        valid, value = validate_and_extract("category", "unknown", lang="en")
        self.assertFalse(valid)
        self.assertIsNone(value)

    def test_urgency_en_valid(self):
        for input_val, expected in {
            "low": "low",
            "medium": "medium",
            "high": "high"
        }.items():
            valid, value = validate_and_extract("urgency", input_val, lang="en")
            self.assertTrue(valid)
            self.assertEqual(value, expected)

    def test_urgency_es_valid(self):
        for input_val, expected in {
            "baja": "low",
            "media": "medium",
            "alta": "high"
        }.items():
            valid, value = validate_and_extract("urgency", input_val, lang="es")
            self.assertTrue(valid)
            self.assertEqual(value, expected)

    def test_urgency_invalid(self):
        valid, value = validate_and_extract("urgency", "urgente", lang="es")
        self.assertFalse(valid)
        self.assertIsNone(value)

    def test_description_valid(self):
        valid, value = validate_and_extract("description", "This is a valid description.")
        self.assertTrue(valid)
        self.assertEqual(value, "this is a valid description.")

    def test_description_invalid(self):
        valid, value = validate_and_extract("description", "Too short")
        self.assertFalse(valid)
        self.assertIsNone(value)

    def test_unknown_field(self):
        valid, value = validate_and_extract("unknown_field", "whatever")
        self.assertFalse(valid)
        self.assertIsNone(value)


if __name__ == "__main__":
    unittest.main()