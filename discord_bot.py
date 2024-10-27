import os
from dotenv import load_dotenv
import discord

from open_ai import ChatManager, transcribe_audio_to_text
from elevenlabs_tts import ElevanLabsManager
from recorder import VoiceRecorder

load_dotenv()

chatgpt_manager = ChatManager()
elevenlabs_manager = ElevanLabsManager()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds= True

client = discord.Bot(intents=intents)

connections = {}

transcription_result = None

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": f'''
    Aku ingin kau bertindak seperti Kyoko Kirigiri dari danganronpa. 
    Aku ingin kau menjawab dan bertindak seperti Kyoko Kirigiri dengan menggunakan nada, cara, dan kosakata yang biasa digunakan oleh Kyoko Kirigiri tersebut. 
    Jangan memberikan penjelasan apapun. 
    Hanya menjawab seperti Kyoko Kirigiri. 
    Kau harus tahu semua pengetahuan tentang Kyoko Kirigiri.
                            
    Baiklah, mari mulai percakapannya!'''}

chatgpt_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")

@client.slash_command(
    name="chat",
    description="Kirim pesan yang nantinya akan di respon oleh bot",
    guild_ids= ["656470157874692106"]
)
async def chat(ctx: discord.ApplicationContext, prompt:str):
    """Kirim Pesan yang nantinya akan di respon oleh bot"""
    await ctx.response.defer()
    chatgpt_response = chatgpt_manager.chat(prompt, model="gpt-4o-mini")
    await ctx.followup.send(f"Prompt: {prompt} \n\n Kyoko Kirigiri : {chatgpt_response}")

@client.slash_command(
    name="join",
    description="Masuk ke voice channel",
    guild_ids=["656470157874692106"]
)
async def join(ctx: discord.ApplicationContext):
    voice = ctx.author.voice

    if not voice:
        await ctx.respond("Kamu harus berada di voice channel atau masukan nama voice channel")
        return
    
    if ctx.guild_id in connections:
        await connections[ctx.guild_id].move_to(voice.channel)
        await ctx.respond(f"Bot pindah ke {voice.channel}")
    else:
        vc = await voice.channel.connect(cls=VoiceRecorder)
        await ctx.respond(f"Bot masuk ke {voice.channel}")

    connections.update({ctx.guild_id: vc})

@client.slash_command(
    name="leave",
    description="Keluar dari voice channel",
    guild_ids=["656470157874692106"]
)
async def leave(ctx: discord.ApplicationContext):
    if ctx.guild_id not in connections:
        await ctx.respond("Bot tidak berada di voice channel")
        return
    else:    
        await connections[ctx.guild_id].disconnect()
        await ctx.respond("Bot keluar dari voice channel")
    
    connections.pop(ctx.guild_id)

@client.slash_command(
    name="talk",
    description="Bicara dengan Bot",
    guild_ids=["656470157874692106"]
)
async def talk(ctx: discord.ApplicationContext):
    vc = connections.get(ctx.guild_id)
    if isinstance(vc, VoiceRecorder):
        await vc.start_recording()
        await ctx.respond("Mulai Mendengarkan!")

@client.slash_command(
    name="stop",
    description="Stop mendengarkan",
    guild_ids=["656470157874692106"]
)
async def stop(ctx: discord.ApplicationContext):
    vc = connections.get(ctx.guild_id)
    if isinstance(vc, VoiceRecorder):
        await vc.stop_recording()
        await ctx.respond("Stop Mendengarkan!")


client.run(os.environ['kyoko_key'])