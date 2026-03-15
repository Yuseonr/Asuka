import datetime
from discord.ext import commands, tasks

class TimeEvent(commands.Cog):
    """ Time-based events for Asuka """
    
    def __init__(self, bot):
        self.bot = bot
        self.good_morning.start()
    
    def cog_unload(self):
        self.good_morning.cancel()
    
    """
    Daily good morning message at 8 AM server time
    """
    @tasks.loop(time=datetime.time(8, 0))
    async def good_morning(self):
        channel_id = self.bot.channel_id
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send("Hmph good morning yus, not like I care or anything, but here's your daily update...")

async def setup(bot):
    await bot.add_cog(TimeEvent(bot))