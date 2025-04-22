# app/unittest/test_save_and_load_conversations.py

import unittest
import tempfile
from pathlib import Path
from datetime import datetime
import shutil
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.storage import save_conversation, load_conversations, list_all_orders



class TestSaveAndLoadConversations(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Override DATA_DIR used in the module to point to the test directory
        self.original_data_dir = save_conversation.__globals__["DATA_DIR"]
        save_conversation.__globals__["DATA_DIR"] = Path(self.test_dir)
        load_conversations.__globals__["DATA_DIR"] = Path(self.test_dir)

    def tearDown(self):
        # Restore original DATA_DIR and clean up the temporary directory
        save_conversation.__globals__["DATA_DIR"] = self.original_data_dir
        load_conversations.__globals__["DATA_DIR"] = self.original_data_dir
        shutil.rmtree(self.test_dir)

    def test_save_and_load_conversation_full_format_natural(self):
        conversation = [
            {"role": "system", "text": "System prompt"},
            {"role": "assistant", "text": "Hello!"},
            {"role": "user", "text": "Hi there!"},
        ]
        extracted = {
            "order_number": "ORD99999",
            "category": "shipping",
            "description": "Item hasn't arrived yet",
            "urgency": "high"
        }
        summary = "User reported delayed shipping for order ORD99999."
        mode = "natural"
        lang = "en"

        # Save a new conversation with mode 'natural'
        save_conversation(extracted, conversation, summary, mode, lang)

        # Load the conversations and verify
        data = load_conversations("ORD99999")
        self.assertEqual(len(data), 1)
        entry = data[0]

        self.assertEqual(entry["mode"], mode)
        self.assertEqual(entry["extracted"], extracted)
        self.assertEqual(entry["summary"], summary)
        self.assertEqual(entry["conversation"], conversation)
        self.assertEqual(entry["lang"], lang)

        # Check that the timestamp is in ISO format (including microseconds)
        try:
            datetime.fromisoformat(entry["timestamp"])
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

        # Alternatively, check the format using a regular expression for ISO format
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$"
        if not re.match(iso_pattern, entry["timestamp"]):
            self.fail(f"Timestamp '{entry['timestamp']}' is not in valid ISO 8601 format")

    def test_save_and_load_conversation_full_format_rigid(self):
        conversation = [
            {"role": "system", "text": "System prompt"},
            {"role": "assistant", "text": "Hello!"},
            {"role": "user", "text": "Hi there!"},
        ]
        extracted = {
            "order_number": "ORD99998",
            "category": "shipping",
            "description": "Item has arrived",
            "urgency": "low"
        }
        summary = "User confirmed item has arrived."
        mode = "rigid"
        lang = "en"

        # Save a new conversation with mode 'rigid'
        save_conversation(extracted, conversation, summary, mode, lang)

        # Load the conversations and verify
        data = load_conversations("ORD99998")
        self.assertEqual(len(data), 1)
        entry = data[0]

        self.assertEqual(entry["mode"], mode)
        self.assertEqual(entry["extracted"], extracted)
        self.assertEqual(entry["summary"], summary)
        self.assertEqual(entry["conversation"], conversation)
        self.assertEqual(entry["lang"], lang)

        # Check that the timestamp is in ISO format (including microseconds)
        try:
            datetime.fromisoformat(entry["timestamp"])
        except ValueError:
            self.fail("Timestamp is not in valid ISO format")

        # Alternatively, check the format using a regular expression for ISO format
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$"
        if not re.match(iso_pattern, entry["timestamp"]):
            self.fail(f"Timestamp '{entry['timestamp']}' is not in valid ISO 8601 format")

    def test_list_all_orders(self):
        conversation = [
            {"role": "system", "text": "System prompt"},
            {"role": "assistant", "text": "Hello!"},
        ]
        extracted = {
            "order_number": "ORD12345",
            "category": "shipping",
            "description": "Item has arrived",
            "urgency": "low"
        }
        summary = "User confirmed item has arrived."
        mode = "chat"
        lang = "en"

        # Save a new conversation for a different order number
        save_conversation(extracted, conversation, summary, mode, lang)

        # List all orders and verify the saved order appears
        orders = list_all_orders()  # Corrected this line
        self.assertIn("ORD12345", orders)

if __name__ == "__main__":
    unittest.main()