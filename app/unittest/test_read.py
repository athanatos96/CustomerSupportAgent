# app/unittest/test_read.py


import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.io_comunications import read

class TestRead(unittest.TestCase):
    @patch("builtins.input", return_value="Hello")
    def test_read_text(self, mock_input):
        result = read(">", audio=False)
        self.assertEqual(result, "Hello")

    def test_read_audio_warning(self):
        result = read("Prompt", audio=True)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
