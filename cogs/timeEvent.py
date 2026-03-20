import datetime
import random
from discord.ext import commands, tasks

UTC7 = datetime.timezone(datetime.timedelta(hours=7))

class TimeEvent(commands.Cog):
    """ Time-based events for Asuka """
    
    def __init__(self, bot):
        self.bot = bot
        self.good_morning.start()
        self.random_message.start()
    
    """ 
    No double loop running when cog is reloaded 
    """
    async def cog_unload(self):
        self.good_morning.cancel()
        self.random_message.cancel()
    
    """
    Daily good morning message at 8 AM server time <3
    """
    @tasks.loop(time = datetime.time(hour=8, minute=0, second=0, tzinfo=UTC7))
    async def good_morning(self):
        channel_id = self.bot.event_channel_id
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send("Hmph good morning yus, not like I care or anything, but here's your daily update...")
    
    """
    Message at random time
    """
    @tasks.loop(minutes=1)
    async def random_message(self):
        interval = random.randint(30, 300)
        message_choice = random.randint(1, 4)
        self.random_message.change_interval(minutes=interval)

        if message_choice == 1:
            message = f"Cmon yus, im not going to improve if you arent working on me >< <@{self.bot.owner_id}>"
        elif message_choice == 2:
            message = f"Don't forget to take a break and stretch your legs! You've been working hard :>"
        elif message_choice == 3:
            message = f"Wanna check the market? Maybe there's a good opportunity"
        else:
            message = f"Remember to drink water! Staying hydrated is important for your health and productivity."

        channel_id = self.bot.event_channel_id
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
    
    @good_morning.before_loop
    @random_message.before_loop
    async def before_good_morning(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(TimeEvent(bot))
