# app/llm_modules/ollama_mistral7b.py

import requests
from typing import List, Dict, Optional

class OllamaMistral7B_Model():
    """
    A wrapper class to interact with an Ollama-based language model endpoint,
    specifically using the Mistral 7B variant by default.
    """
    base_url: str = "http://localhost:11434"
    model: str = "mistral:7b-text-fp16" #"mistral-small:22b-instruct-2409-fp16"#"llama3.2:3b-text-fp16 "#"mistral:7b-text-fp16"

    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None) -> None:
        """
        Initializes the model with optional overrides for the model name and base URL.
        
        Args:
            model (Optional[str]): A custom model name to override the default.
            base_url (Optional[str]): A custom base URL for the Ollama API.
        """
        if model:
            self.set_model(model)
        if base_url:
            self.set_base_url(base_url)

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        """
        Sends a formatted chat prompt to the Ollama API and retrieves a response.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries, each with 'role' and 'content'.
            temperature (float): Sampling temperature for generation (controls randomness).

        Returns:
            str: The assistant's response text.
        """
        prompt = self._format_prompt(messages)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["response"].strip()

    def set_model(self, model: str) -> None:
        """
        Sets the model name used for inference.
        
        Args:
            model (str): The name of the model to use.
        """
        self.model = model

    def get_model(self) -> str:
        """
        Retrieves the currently set model name.

        Returns:
            str: The name of the model in use.
        """
        return self.model

    def set_base_url(self, base_url: str) -> None:
        """
        Sets the base URL of the Ollama API endpoint.

        Args:
            base_url (str): The new base URL to use.
        """
        self.base_url = base_url

    def _format_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Formats a list of message dictionaries into a single prompt string 
        using role-specific tags.

        Args:
            messages (List[Dict[str, str]]): Messages with 'role' and 'content'.

        Returns:
            str: A formatted prompt string for the LLM.
        """
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"[System]\n{content}\n"
            elif role == "user":
                prompt += f"[User]\n{content}\n"
            elif role == "assistant":
                prompt += f"[Assistant]\n{content}\n"
            elif role == "developer":
                prompt += f"[Developer]\n{content}\n"
        prompt += "[Assistant]\n"
        return prompt
