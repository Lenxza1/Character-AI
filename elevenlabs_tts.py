import os
from dotenv import load_dotenv
from elevenlabs import generate, play, set_api_key, voices

load_dotenv()

client = set_api_key(api_key=os.environ['elevenlabs_api'])

class ElevanLabsManager:
    def __init__(self) -> None:
        all_voices = voices()

    def text_to_speech(self, msg, voice):
        audio = generate(
            text=msg,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        play(audio)
