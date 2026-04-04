from discord.ext import commands
from services.simple_ai import asuka_response

class messageHandler(commands.Cog):
    """ Handle incoming message for Asuka """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if "asuka" in message.content.lower():
            # await message.channel.send(f"Hmph u called me? what do you want, <@{message.author.id}>?")
            async with message.channel.typing():
                response = await asuka_response(message.content)
            await message.channel.send(response)
        
        elif message.content.lower() == "good night":
            await message.channel.send("Hmph, whatever. Make sure your code actually compiles before you sleep.")
    

async def setup(bot):
    await bot.add_cog(messageHandler(bot))