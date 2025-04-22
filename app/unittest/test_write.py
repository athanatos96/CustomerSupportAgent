# app/unittest/test_write.py

#################
## DEPRECIATED ##
#################
# Use test_user_io.py instead

import unittest
from io import StringIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.io_comunications import write

class TestWrite(unittest.TestCase):
    def test_write_text(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        write("Hello", audio=False)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "Hello")

    def test_write_audio_warning(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        write("Hello", audio=True)
        sys.stdout = sys.__stdout__
        self.assertIn("Audio mode not implemented", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
