import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, play, save
from rich import print
from typing import Literal
from dataclasses import dataclass

load_dotenv()

@dataclass
class VoiceSettings:
    stability: int = 0.50
    similarity_boost: int = 0.75
    speed: float = 1.2

class ElevanLabsManager:
    def __init__(self) -> None:
        self.client = ElevenLabs(api_key=os.environ['elevenlabs_api'])
        self.all_voices = self.client.voices.search()
        self.voice_settings = VoiceSettings()
        print("[green]Available voices:")
        for voice in self.all_voices.voices:
            print(f"[green] - {voice.name} ({voice.voice_id})")
        self.models = self.client.models.get_all()
        print("[green]Available models:")
        for model in self.models:
            print(f"[green] - {model.name} ({model.model_id})")
        print("[green]Eleven Labs TTS initialized.")


    def text_to_speech(self, msg: str, voice_id: str = "iWydkXKoiVtvdn4vLKp9", model: str = "eleven_turbo_v2_5"):
        """Convert text to speech using Eleven Labs API."""
        try:
            audio = self.client.text_to_speech.convert(text=msg, voice_id=voice_id, output_format="opus_48000_32", model_id=model, voice_settings=self.voice_settings)
            if not os.path.exists("audio"):
                os.makedirs("audio")
            return audio
        except Exception as e:
            print(f"[red]Error in Eleven Labs TTS: {e}")
            return None


if __name__ == "__main__":
    elevenlabs_manager = ElevanLabsManager()
    elevenlabs_manager.text_to_speech("Hello, this is a test message.")
    print("[green]Audio saved as audio/elevenlabs.mp3")