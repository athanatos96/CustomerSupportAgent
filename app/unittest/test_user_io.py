# app/unittest/test_user_io.py

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.utils.io_comunications import UserIO


class TestUserIO(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MagicMock()
        self.mock_llm.transcribe_audio.return_value = "This is a test"
        self.mock_llm.text_to_speech.return_value = b"audio data"
        self.io = UserIO(llm_model=self.mock_llm, verbose=False)

    @patch("builtins.input", return_value="Hello")
    def test_read_text_mode(self, mock_input):
        result = self.io.read(">", audio=False)
        self.assertEqual(result, "Hello")
        mock_input.assert_called_once()

    @patch("app.utils.io_comunications.os.path.exists", return_value=True)
    @patch("app.utils.io_comunications.record_audio_until_silence", return_value="fake_audio.wav")
    @patch("app.utils.io_comunications.os.remove")
    def test_read_audio_mode_success(self, mock_remove, mock_record_audio, mock_exists):
        result = self.io.read("Prompt", audio=True)
        self.assertEqual(result, "This is a test")
        self.mock_llm.transcribe_audio.assert_called_once_with("fake_audio.wav")
        mock_remove.assert_called_once_with("fake_audio.wav")

    @patch("app.utils.io_comunications.os.path.exists", return_value=True)
    @patch("app.utils.io_comunications.record_audio_until_silence", return_value="fake_audio.wav")
    @patch("app.utils.io_comunications.os.remove")
    def test_read_audio_mode_exception(self, mock_remove, mock_record_audio, mock_exists):
        self.mock_llm.transcribe_audio.side_effect = Exception("Transcription failed")
        result = self.io.read("Prompt", audio=True)
        self.assertEqual(result, "")  # Should return empty string on error
        mock_remove.assert_called_once_with("fake_audio.wav")

    def test_write_text_mode(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.io.write("Hello world", audio=False)
        sys.stdout = sys.__stdout__
        self.assertIn("Hello world", captured_output.getvalue())

    @patch("app.utils.io_comunications.AudioPlayer")
    def test_write_audio_mode(self, mock_audio_player_class):
        mock_audio_player = MagicMock()
        mock_audio_player_class.return_value = mock_audio_player

        self.io.write("Hello audio", audio=True)

        self.mock_llm.text_to_speech.assert_called_once_with("Hello audio")
        mock_audio_player.add_audio.assert_called_once_with(b"audio data")
        mock_audio_player.wait_for_completion.assert_called_once()


if __name__ == '__main__':
    unittest.main()
