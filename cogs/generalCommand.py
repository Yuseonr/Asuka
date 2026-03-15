import discord
import time
from discord import app_commands
from discord.ext import commands

class GeneralCommands(commands.Cog):
    """ General commands fo Asuka """

    def __init__(self, bot):
        self.bot = bot
    
    """ 
    Ping Asuka get latency 
    """
    @app_commands.command(name="ping", description="Test Asuka latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"umm.. so latency is {latency}ms")

    """ 
    Asuka status and profile 
    """
    @app_commands.command(name="status", description="See Asuka profile and status")
    async def status(self, interaction: discord.Interaction):
        uptime_seconds = int(time.time() - self.bot.start_time)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        uptime = f"{d}d {h}h {m}m {s}s"

        embed = discord.Embed(
            title="Asuka Status ><", 
            color=discord.Color.red() 
        )
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.set_footer(text="Asuka Bot made with ❤️")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    
    """ 
    Set channel for time-based events
    """
    @app_commands.command(name="setup", description="Set the channel for time-based events")
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.bot.channel_id = channel.id
        await interaction.response.send_message(f"Channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))