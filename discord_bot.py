import os
from dotenv import load_dotenv
import discord

from chat_gpt import ChatManager
from elevenlabs_tts import ElevanLabsManager

load_dotenv()

chatgpt_manager = ChatManager()
elevenlabs_manager = ElevanLabsManager()


intents = discord.Intents.default()
intents.message_content = True
intents.guilds= True

client = discord.Bot(intents=intents)

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
    name="message",
    description="Kirim pesan yang nantinya akan di respon oleh bot",
    guild_ids= ["656470157874692106"]
)
async def message(ctx: discord.ApplicationContext, prompt:str):
    """Kirim Pesan yang nantinya akan di respon oleh bot"""
    await ctx.response.defer()
    chatgpt_response = chatgpt_manager.chat(prompt)
    await ctx.followup.send(chatgpt_response)

@client.slash_command(
    name="join",
    description="Masuk ke voice channel",
    guild_ids= ["656470157874692106"]
)
async def join(ctx: discord.ApplicationContext):
    pass
    

client.run(os.environ['kyoko_key'])