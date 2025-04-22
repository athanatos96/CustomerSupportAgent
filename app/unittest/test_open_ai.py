# app/unittest/test_open_ai.py


import unittest
from unittest.mock import patch, Mock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.llm_modules.open_ai import OpenAI_Model
from openai import OpenAI

class TestOpenAIModel(unittest.TestCase):
    
    @patch("app.llm_modules.open_ai.OpenAI")
    def test_initialization_with_custom_client(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        model_name = "gpt-4.1-nano"
        
        # Act
        openai_model = OpenAI_Model(model=model_name, client=mock_client)
        
        # Assert
        self.assertEqual(openai_model.get_model(), model_name)
        self.assertEqual(openai_model.client, mock_client)

    @patch("app.llm_modules.open_ai.OpenAI")
    def test_initialization_with_default_client(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        mock_client.responses.create.return_value.output_text = "Mocked response"
        
        # Act
        openai_model = OpenAI_Model(model=None, client=None)  # No custom client
        openai_model.set_client(mock_client)  # Using the default client
        
        # Assert
        self.assertEqual(openai_model.client, mock_client)  # Assert that the client is set correctly
        mock_client.responses.create.assert_not_called()  # Ensure the mock client hasn't been called yet
        self.assertEqual(openai_model.get_model(), "gpt-4.1-nano")  # Default model
    
    @patch("app.llm_modules.open_ai.OpenAI")
    @patch.object(OpenAI_Model, 'chat')
    def test_chat_method(self, mock_chat, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        openai_model = OpenAI_Model(client=mock_client)
        
        # Simulate the response for the chat method
        mock_chat.return_value = "Hello there!"
        messages = [{"role": "user", "content": "Say hello!"}]
        
        # Act
        response = openai_model.chat(messages)
        
        # Assert
        self.assertEqual(response, "Hello there!")
        mock_chat.assert_called_once_with(messages)
    
    @patch("app.llm_modules.open_ai.OpenAI")
    def test_set_model(self, MockOpenAI):
        # Arrange
        model_name = "gpt-4.1-nano"
        openai_model = OpenAI_Model(model=model_name)
        
        # Act
        openai_model.set_model("gpt-4.0")
        
        # Assert
        self.assertEqual(openai_model.get_model(), "gpt-4.0")
    
    @patch("app.llm_modules.open_ai.OpenAI")
    def test_set_client(self, MockOpenAI):
        # Arrange
        mock_client = MockOpenAI.return_value
        openai_model = OpenAI_Model(client=None)  # Initialize with no client
        
        # Act
        openai_model.set_client(mock_client)
        
        # Assert
        self.assertEqual(openai_model.client, mock_client)

if __name__ == "__main__":
    unittest.main()
