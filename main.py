import os
import discord
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class AsukaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

        self.start_time = time.time()  
        self.channel_id = None

    async def setup_hook(self):
        await self.load_extension("cogs.generalCommand")
        await self.load_extension("cogs.adminCommand")
        await self.load_extension("cogs.timeEvent")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

if __name__ == "__main__":
    asuka = AsukaBot()
    asuka.run(TOKEN)