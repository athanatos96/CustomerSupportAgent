# app/utils/audio_utils.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write as wav_write
import tempfile
import time
import threading  # For handling threads
import queue  # For creating and managing queues
import pyaudio

def record_audio_until_silence(
    sample_rate=44100,
    silence_threshold=5,
    silence_duration=2.0,
    max_duration=60,
    verbose=True
) -> str:
    """
    Records audio until silence is detected for a given duration.

    Args:
        sample_rate (int): Sampling rate.
        silence_threshold (int): Threshold for detecting silence (lower = more sensitive).
        silence_duration (float): How long to wait in seconds before stopping on silence.
        max_duration (int): Max recording time in seconds (safety stop).

    Returns:
        str: Path to temporary .wav file.
    """
    print("🎤 Speak to start recording (will stop after silence)...")

    chunk_duration = 0.2  # seconds
    chunk_samples = int(sample_rate * chunk_duration)

    recorded_audio = []
    silence_start = None
    start_time = time.time()

    stream = sd.InputStream(samplerate=sample_rate, channels=1)
    stream.start()

    try:
        while True:
            if time.time() - start_time > max_duration:
                print("⏱️ Max duration reached.")
                break

            chunk, _ = stream.read(chunk_samples)
            chunk = np.squeeze(chunk)
            recorded_audio.append(chunk)

            rms = np.sqrt(np.mean(chunk**2)) * 1000
            if verbose:
                # Print current audio level and silence duration
                if silence_start is not None:
                    current_silence_duration = time.time() - silence_start
                else:
                    current_silence_duration = 0
                print(f"Audio level: {rms}, silence_threshold: {silence_threshold}, silence_duration_threshold: {silence_duration}, current_silence_duration: {current_silence_duration:.2f}s")
            if rms < silence_threshold:
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start >= silence_duration:
                    print("🛑 Silence detected. Stopping...")
                    break
            else:
                silence_start = None
    finally:
        stream.stop()
        stream.close()

    audio_data = np.concatenate(recorded_audio, axis=0)
    tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav_write(tmp_file.name, sample_rate, audio_data.astype(np.float32))
    return tmp_file.name


class AudioPlayer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.playback_complete = threading.Event()
        self.audio_added = threading.Event()
        
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True)
        
        # Start audio playback thread
        self.audio_thread = threading.Thread(target=self.play_audio)
        self.audio_thread.start()

    def play_audio(self):
        while not self.playback_complete.is_set():
            try:
                audio_chunk = self.audio_queue.get(timeout=0.1)
                self.stream.write(audio_chunk)
            except queue.Empty:
                if self.audio_added.is_set() and self.audio_queue.empty():
                    # If all audio has been added and queue is empty, we're done
                    break
                continue

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        #print("Audio playback completed.")

    def add_audio(self, audio_data):
        for chunk in audio_data:
            self.audio_queue.put(chunk)
        self.audio_added.set()  # Signal that all audio has been added

    def wait_for_completion(self):
        self.audio_thread.join()