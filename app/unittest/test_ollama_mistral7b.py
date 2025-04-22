# app/unittest/test_ollama_mistral7b.py

import unittest
from unittest.mock import patch, Mock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.llm_modules.ollama_mistral7b import OllamaMistral7B_Model


class TestOllamaMistral7BModel(unittest.TestCase):

    def setUp(self):
        self.model = OllamaMistral7B_Model()

    def test_set_and_get_model(self):
        self.model.set_model("custom-model")
        self.assertEqual(self.model.get_model(), "custom-model")

    def test_set_base_url(self):
        self.model.set_base_url("http://testserver:1234")
        self.assertEqual(self.model.base_url, "http://testserver:1234")

    def test_format_prompt(self):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke."},
            {"role": "assistant", "content": "Why did the chicken cross the road?"},
        ]
        formatted = self.model._format_prompt(messages)
        expected = (
            "[System]\nYou are a helpful assistant.\n"
            "[User]\nTell me a joke.\n"
            "[Assistant]\nWhy did the chicken cross the road?\n"
            "[Assistant]\n"
        )
        self.assertEqual(formatted, expected)

    @patch("app.llm_modules.ollama_mistral7b.requests.post")
    def test_chat_response(self, mock_post):
        # Arrange
        messages = [
            {"role": "user", "content": "Say hello!"}
        ]
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Hello there!"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Act
        response = self.model.chat(messages)

        # Assert
        self.assertEqual(response, "Hello there!")
        mock_post.assert_called_once()
        called_url = mock_post.call_args[0][0]
        self.assertTrue(called_url.endswith("/api/generate"))
        self.assertIn("model", mock_post.call_args[1]["json"])


if __name__ == "__main__":
    unittest.main()
