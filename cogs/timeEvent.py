import datetime
from discord.ext import commands, tasks

UTC7 = datetime.timezone(datetime.timedelta(hours=7))

class TimeEvent(commands.Cog):
    """ Time-based events for Asuka """
    
    def __init__(self, bot):
        self.bot = bot
        self.good_morning.start()
    
    """ 
    No double loop running when cog is reloaded 
    """
    async def cog_unload(self):
        self.good_morning.cancel()
    
    """
    Daily good morning message at 8 AM server time <3
    """
    @tasks.loop(time = datetime.time(hour=8, minute=0, second=0, tzinfo=UTC7))
    async def good_morning(self):
        channel_id = self.bot.event_channel_id
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send("Hmph good morning yus, not like I care or anything, but here's your daily update...")

async def setup(bot):
    await bot.add_cog(TimeEvent(bot))