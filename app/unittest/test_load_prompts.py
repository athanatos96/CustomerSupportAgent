# app/unittest/test_load_prompts.py

import unittest
import tempfile
import os
import json

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.prompt_loader import load_prompts



class TestLoadPrompts(unittest.TestCase):

    def test_load_customer_support_en(self):
        prompts = load_prompts("customer_support", "en")
        self.assertIsInstance(prompts, dict)
        self.assertIn("system_prompt", prompts)
        self.assertIn("questions", prompts)
        self.assertIn("order_number", prompts["questions"])

    def test_load_customer_support_es(self):
        prompts = load_prompts("customer_support", "es")
        self.assertIsInstance(prompts, dict)
        self.assertIn("questions", prompts)
        self.assertEqual(prompts["questions"]["urgency"], "¿Qué nivel de urgencia tiene esto? (baja, media, alta)")

    def test_load_supervisor_en(self):
        prompts = load_prompts("supervisor", "en")
        self.assertIsInstance(prompts, dict)
        self.assertIn("role_intro", prompts)
        self.assertIn("fix_notes", prompts)

    def test_load_supervisor_es(self):
        prompts = load_prompts("supervisor", "es")
        self.assertIsInstance(prompts, dict)
        self.assertIn("role_intro", prompts)
        self.assertIn("fix_prompt", prompts)

    def test_invalid_agent(self):
        with self.assertRaises(FileNotFoundError):
            load_prompts("non_existent_agent", "en")

    def test_invalid_lang(self):
        with self.assertRaises(FileNotFoundError):
            load_prompts("customer_support", "fr")  # Assuming French file doesn't exist


if __name__ == "__main__":
    unittest.main()
