# app/llm_modules/open_ai.py

from openai import OpenAI
from typing import List, Dict
import os

class OpenAI_Model():
    """
    A class to interact with OpenAI's GPT model and Text-to-Speech (TTS) API through the OpenAI API client.

    Attributes:
        client (OpenAI): An instance of the OpenAI client to interact with the API.
        model (str): The model name to be used for generating responses (default is "gpt-4.1-nano").

    Methods:
        __init__(self, model: str = None, client: OpenAI = None) -> None:
            Initializes the OpenAI_Model with the given model and OpenAI client.
        
        chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
            Sends the messages to the OpenAI API and returns the generated response.

        set_client(self, client: OpenAI) -> None:
            Sets the OpenAI client instance.

        set_model(self, model: str) -> None:
            Sets the model name to be used for generating responses.

        get_model(self) -> str:
            Retrieves the current model name.

        transcribe_audio(self, audio_path: str, model: str = "whisper-1") -> str:
            Transcribes an audio file using OpenAI's Whisper model.
        
        text_to_speech(self, text: str, speech_file_path: str, voice: str = "coral", instructions: str = "Speak in a cheerful and positive tone.") -> None:
            Converts text to speech using OpenAI's TTS API and saves the result to the specified file.
    """
    client = None
    model = "gpt-4.1-nano"

    def __init__(self, model:str = None, client:OpenAI = None) -> None:
        """
        Initializes the OpenAI_Model with the specified model and OpenAI client.

        Args:
            model (str, optional): The model to be used for generating responses. Defaults to "gpt-4.1-nano".
            client (OpenAI, optional): The OpenAI client instance. If None, a new OpenAI client is created.
        """
        # Set the model name
        if model:
            self.set_model(model)

        # Set the Open AI client
        if client:
            self.set_client(client)
        else:
            self.set_client(OpenAI())
    

    def chat(self, messages: List[Dict], temperature: float = 0.3) -> str:
        """
        Sends the provided messages to the OpenAI API and returns the generated response.

        Args:
            messages (List[Dict]): A list of message dictionaries where each dictionary contains 'role' and 'content'.
            temperature (float, optional): A value that controls the randomness of the model's output. Defaults to 0.3.

        Returns:
            str: The generated response text from the model.
        """
        response = self.client.responses.create(
                        model=      self.model,
                        input=      messages,
                        temperature=temperature,
        )
        return response.output_text
    
    def transcribe_audio(self, audio_path: str, model: str = "whisper-1") -> str:
        """
        Transcribes an audio file using OpenAI's Whisper model.

        Args:
            audio_path (str): Path to the local audio file.
            model (str): Whisper model to use (default: "whisper-1").

        Returns:
            str: The transcribed text.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        with open(audio_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            return transcript

    def text_to_speech(self, text: str, voice: str = "coral", instructions: str = "Speak in a cheerful and positive tone.", model: str = "gpt-4o-mini-tts") -> None:
        """
        Converts text to speech using OpenAI's TTS API and returns the audio.

        Args:
            text (str): The text to convert to speech.
            voice (str): The voice to use for speech (default is "coral").
            instructions (str): Instructions on how the speech should sound (default is "Speak in a cheerful and positive tone.").
            model (str): Selected model, default gpt-4o-mini-tts
        """
        audio_response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            instructions=instructions,
            response_format="pcm"
        )
        return audio_response.iter_bytes(chunk_size=1024)

    def set_client(self, client:OpenAI) -> None:
        """
        Sets the OpenAI client instance to be used for API communication.

        Args:
            client (OpenAI): The OpenAI client instance.
        """
        self.client = client
    
    def set_model(self, model:str) -> None:
        """
        Sets the model name to be used for generating responses.

        Args:
            model (str): The model name to be used.
        """
        self.model = model

    def get_model(self)->str:
        """
        Retrieves the current model name.

        Returns:
            str: The current model name.
        """
        return self.model