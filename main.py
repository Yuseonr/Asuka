import discord
import os
from discord import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}, Asuka ready!")
    
    async def on_message(self, message : Message):
        if message.author == client.user:
            return
        
        if message.content.startswith("Hello"):
            await message.channel.send(f'Hi there @{message.author} good to see you:)')

        print(f"Message from @{message.author} from channel {message.channel} : {message.content}")

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(TOKEN)


