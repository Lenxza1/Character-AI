import discord
import opuslib
import wave
import io
import discord.opus

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus.dll')

class VoiceRecorder(discord.VoiceClient):
    def __init__(self, client, channel):
        super().__init__(client, channel)
        self.client = client
        self.channel = channel
        self.recording = False
        self.audio_buffer = io.BytesIO()
        self.decoder = opuslib.Decoder(48000, 2)

    async def start_recording(self):
        self.recording = True

    async def stop_recording(self):
        self.recording = False
        with wave.open('recording.wav', 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2) 
            wf.setframerate(48000)
            wf.writeframes(self.audio_buffer.getvalue())

    async def receive_audio(self, data):
        if self.recording:
            pcm_data = self.decoder.decode(data, frame_size=960)
            self.audio_buffer.write(pcm_data)




# import discord
# import opuslib
# import wave
# import io
# import discord.opus

# if not discord.opus.is_loaded():
#     discord.opus.load_opus('opus.dll')

# class VoiceRecorder(discord.VoiceClient):
#     def __init__(self, client, channel):
#         super().__init__(client, channel)
#         self.client = client
#         self.channel = channel
#         self.recording = False
#         self.audio_buffer = io.BytesIO()
#         self.decoder = opuslib.Decoder(48000, 2)

#     async def on_voice_server_update(self, data):
#         await super().on_voice_server_update(data)

#     async def on_voice_state_update(self, data):
#         await super().on_voice_state_update(data)

#     async def connect(self, *, timeout, reconnect):
#         await super().connect(timeout=timeout, reconnect=reconnect)

#     async def disconnect(self, *, force=False):
#         await super().disconnect(force=force)

#     async def start_recording(self):
#         self.recording = True

#     async def stop_recording(self):
#         self.recording = False
#         with wave.open('recording.wav', 'wb') as wf:
#             wf.setnchannels(2)
#             wf.setsampwidth(2)
#             wf.setframerate(48000)
#             wf.writeframes(self.audio_buffer.getvalue())

#     async def receive_audio(self, data):
#         if self.recording:
#             pcm_data = self.decoder.decode(data, frame_size=960)
#             self.audio_buffer.write(pcm_data)