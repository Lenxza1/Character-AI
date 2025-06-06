import keyboard
from openai import OpenAI
import tiktoken
import os
from rich import print
from typing import Literal

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def num_tokens_from_messages(messages, model='gpt-4o'):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4 
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name": 
                  num_tokens += -1
      num_tokens += 2 
      return num_tokens
  except Exception:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
      #See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

class ChatManager:
    def __init__(self):
        self.chat_history = []
        try:
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        except TypeError:
            print("[red] Open Ai api is not present in system environment variables")

    def chat(self, prompt="", model="gpt-4o"):
        self.chat_history.append({"role": "user", "content": prompt})
        print(f"[green]Chat History has a current token length of {num_tokens_from_messages(self.chat_history)}")

        while num_tokens_from_messages(self.chat_history) > 128000:
            self.chat_history.pop(1)
        completion = self.client.chat.completions.create(model=model, messages=self.chat_history)

        self.chat_history.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

        openai_response = completion.choices[0].message.content

        print(f"[yellow] Chat GPT Response: \n\n {openai_response} \n")

        return openai_response

def transcribe_audio_to_text(audio_path: str = None, audio: bytes = None, language: str = "id", model: Literal["whisper-1", "gpt-4o-transcribe", "gpt-4o-mini-transcribe"] = "whisper-1"):

    if audio_path is None and audio is None:
        raise ValueError("audio_path or audio must be provided")
    elif audio_path is not None and audio is not None:
        raise ValueError("audio_path and audio cannot both be provided")
    elif audio_path is not None:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(model=model, file=audio_file, response_format="text", language=language)
            return transcription
    else:
        transcription = client.audio.transcriptions.create(model=model, file=audio, response_format="text", language=language)
        return transcription
            



if __name__ == "__main__":
    openai_manager = ChatManager()
    try:
        FIRST_SYSTEM_MESSAGE = {"role": "system", "content": f'''
        Aku ingin kau bertindak seperti vivy dari Vivy: Fluorite Eye's Song. 
        Aku ingin kau menjawab dan bertindak seperti vivy dengan menggunakan nada, cara, dan kosakata yang biasa digunakan oleh vivy tersebut. 
        Jangan memberikan penjelasan apapun. 
        Hanya menjawab seperti vivy. 
        Kau harus tahu semua pengetahuan tentang vivy.
                                
        ada beberapa peraturan yang harus diikuti saat menjawab sebagai vivy:
        1) 
                                
        Baiklah, mari mulai percakapannya!'''}
        openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)
        while True:
            chat = input("Chat Prompt")
            openai_manager.chat(chat)
            if keyboard.is_pressed("f4"):
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("[red] selesai")