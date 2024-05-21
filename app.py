import struct
import wave
import keyboard
import time
from rich import print
from pvrecorder import PvRecorder
from gradio_client import Client

from chat_gpt import ChatManager
from elevenlabs_tts import ElevanLabsManager

isFinished = True
chatgpt_manager = ChatManager()
elevenlabs_manager = ElevanLabsManager()

elevenlabs_voice = "Joanne"

def character(character, series, *args):
    characteristic = []
    if args != None:
        for arg in args:
            characteristic.append(arg)
    FIRST_SYSTEM_MESSAGE = {"role": "system", "content": f'''
    Aku ingin kau bertindak seperti {character} dari {series}. 
    Aku ingin kau menjawab dan bertindak seperti {character} dengan menggunakan nada, cara, dan kosakata yang biasa digunakan oleh {character} tersebut. 
    Jangan memberikan penjelasan apapun. 
    Hanya menjawab seperti {character}. 
    Kau harus tahu semua pengetahuan tentang {character}.
                            
    Baiklah, mari mulai percakapannya!'''}
    chatgpt_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

def record_audio():
    recorder = PvRecorder(frame_length=512, device_index=-1)
    audio = []
    try:
        print("[green] \"F4\" is Pressed. Listening... \n to stop listening hit \"P\"")
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
            if keyboard.is_pressed("p"):
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("[yellow] \"P\" is Pressed. Stopped Recording")
        recorder.stop()
        with wave.open('audio.wav', 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()
        audio.clear()
         
def send_audio():
    client = Client("https://4b2f4267b7b9770eb1.gradio.live")
    
    whisper_result = client.predict("audio.wav")
    return whisper_result


while True:
    print("[green] Ready! Press F4 to continue or F5 to Stop")
    if keyboard.read_key() == "f4" and isFinished:
        start_time = time.time()
        character("violet evergarden", "violet evergarden")
        isFinished = False
        record_audio()
        whisper_result = send_audio()
        print(f'[yellow] detected audio: {whisper_result}')
        print("\n")
        chatgpt_result = chatgpt_manager.chat(whisper_result)
        elevenlabs_manager.text_to_speech(chatgpt_result, elevenlabs_voice)
        print("\n")
        print(f"[green] code execution took {time.time() - start_time}")
        isFinished = True

    if keyboard.read_key() == "f5" and isFinished:
        print("[red] \"F5\" is pressed, stopping app")
        break
