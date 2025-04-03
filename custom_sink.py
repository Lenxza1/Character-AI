import discord
import wave
import io
import os

class CustomSink(discord.sinks.WaveSink):
    """Custom sink to record audio data and save to recording.wav.

    Parameters
    ----------
    callback: :class:`callable`
        The function to call when the audio data is finished writing.
    channel: :class:`discord.TextChannel`
        The channel to send the audio data to.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_buffer = io.BytesIO()
        
    def cleanup(self):
        """Cleans up the sink and saves recording.wav"""
        super().cleanup()
        
        self.save_to_wav()
        
    def save_to_wav(self):
        """Saves all recorded audio to audio/recording.wav and individual user files"""
        if not os.path.exists('audio'):
            os.makedirs('audio')
        
        for user_id, audio_data in self.audio_data.items():
            audio_data.file.seek(0)
            user_filename = f'audio/user_{user_id}.wav'
            
            with wave.open(user_filename, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes(audio_data.file.read())
            
            audio_data.file.seek(0)
        
        combined_audio = io.BytesIO()
        for user_id, audio_data in self.audio_data.items():
            audio_data.file.seek(0)
            combined_audio.write(audio_data.file.read())
        
        combined_filename = 'audio/recording.wav'
        with wave.open(combined_filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(48000)
            combined_audio.seek(0)
            wf.writeframes(combined_audio.getvalue())
                        
    def reset(self):
        """Resets the sink."""
        self.audio_data = {}
        self.finished = False
        self.audio_buffer = io.BytesIO()
        return self