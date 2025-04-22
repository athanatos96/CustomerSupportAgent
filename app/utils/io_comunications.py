# app/utils/io_comunications.py
from app.utils.audio_utils import AudioPlayer, record_audio_until_silence
import os


class UserIO:
    def __init__(self, llm_model=None, verbose: bool = True, 
                 silence_duration: float = 2.0, max_duration: int = 60, 
                 silence_threshold: int = 5):
        """
        Initializes the UserIO class.

        Args:
            llm_model: An instance of the LLM model that supports audio transcription.
            verbose (bool): If True, prints status messages. If False, stays quiet.
            silence_duration (float): How long to wait in seconds before stopping on silence.
            max_duration (int): Max recording time in seconds.
            silence_threshold (int): Threshold for detecting silence (lower = more sensitive).
        """
        self.llm_model = llm_model
        self.verbose = verbose
        self.silence_duration = silence_duration
        self.max_duration = max_duration
        self.silence_threshold = silence_threshold

    def read(self, prefix: str, audio: bool = False) -> str:
        """
        Reads input from the user, either via keyboard or microphone.

        Args:
            prefix (str): A string to display before prompting.
            audio (bool): Whether to use audio input.

        Returns:
            str: User input (typed or transcribed).
        """
        if audio:
            if self.verbose:
                print(prefix + "🎤 (Audio mode)")
            audio_path = record_audio_until_silence(
                silence_duration=self.silence_duration,
                max_duration=self.max_duration,
                silence_threshold=self.silence_threshold,
                verbose=self.verbose
            )

            try:
                transcription = self.llm_model.transcribe_audio(audio_path)
                if self.verbose:
                    print("📄 Transcription:", transcription)
            except Exception as e:
                print(f"[ERROR] Failed to transcribe audio: {e}")
                transcription = ""
            finally:
                if os.path.exists(audio_path):
                    os.remove(audio_path)

            # Convert text to speech (audio mode)
            print(f"[INFO] Converting speach to text: {transcription}")

            return transcription.strip()
        else:
            if self.verbose:
                print("📄 (Text mode)")
            return input(prefix).strip()
        


    def write(self, msg: str, audio:bool = False) -> None:
        """
        Print a message to the console. Optionally supports audio mode (not implemented).

        Args:
            msg (str): The message to print.
            audio (bool): Whether to use audio output (currently not implemented).
        """

        if audio:
            if self.verbose:
                print(f"🎤 (Audio mode) {msg}")
            # Convert text to speech (audio mode)
            print(f"[INFO] Converting text to speech: {msg}")
            

            # Generate audio from text using LLM model
            audio_data = self.llm_model.text_to_speech(msg)

            if self.verbose:
                print(f"🎤 Play Audio")
            # Initialize AudioPlayer to play the audio
            player = AudioPlayer()
            player.add_audio(audio_data)

            # Wait for audio to finish playing
            player.wait_for_completion()
            if self.verbose:
                print(f"🎤 Finished Audio")
        else:
            if self.verbose:
                print(f"📄 (Text mode)")
            print(msg)


'''
def write(msg: str, audio=False) -> None:
    """
    Print a message to the console. Optionally supports audio mode (not implemented).

    Args:
        msg (str): The message to print.
        audio (bool): Whether to use audio output (currently not implemented).
    """

    if audio:
        # TODO
        # Be carefull with emojis

        print(f"[WARNING] Audio mode not implemented")
        pass
    else:
        print(msg)

def read(prefix: str, audio=False) -> str:
    """
    Read input from the user. Optionally supports audio mode (not implemented).

    Args:
        prefix (str): A string to display before the input prompt.
        audio (bool): Whether to use audio input (currently not implemented).

    Returns:
        str: The user input.
    """
    if audio:
        # TODO
        print(f"[WARNING] Audio mode not implemented")
        user_input = ""
        pass
    else:
        user_input = input(prefix).strip()

    return user_input'''