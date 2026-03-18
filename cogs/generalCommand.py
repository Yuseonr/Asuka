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
        embed.add_field(name="Event Channel", value=f"<#{self.bot.event_channel_id}>" if self.bot.event_channel_id else "Not Set", inline=True)
        embed.add_field(name="Signal Channel", value=f"<#{self.bot.trading_channel_id}>" if self.bot.trading_channel_id else "Not Set", inline=True)
        embed.set_footer(text="Asuka Bot made with ❤️")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    
    """ 
    Asuka set channel for time-based events and/or signal notifications
    """
    @app_commands.command(name="set_channel", description="Set Asuka to channel for time-based events and/or signal notifications")
    @app_commands.choices(channel_type=[
        app_commands.Choice(name="Event & Signal", value="all"),
        app_commands.Choice(name="Event Only", value="event"),
        app_commands.Choice(name="Trading Only", value="trading")
    ])
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, channel_type: app_commands.Choice[str]):
        selected = channel_type.value
        if selected == "all":
            self.bot.event_channel_id = channel.id
            self.bot.trading_channel_id = channel.id
            await interaction.response.send_message(f"**All** channel set to {channel.mention}")
        elif selected == "event":
            self.bot.event_channel_id = channel.id
            await interaction.response.send_message(f"**Event** channel set to {channel.mention}")
        elif selected == "trading":
            self.bot.trading_channel_id = channel.id
            await interaction.response.send_message(f"**Trading** channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))