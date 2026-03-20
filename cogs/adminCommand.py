from discord.ext import commands
from discord.ext.commands import Context, ExtensionNotLoaded

class AdminCommands(commands.Cog):
    """ Admin commands for Asuka """

    def __init__(self, bot):
        self.bot = bot

    """
    Reload or load spesific cog
    """
    @commands.command(name="reload")
    @commands.is_owner() 
    async def reload_cogs(self, ctx: Context, cog: str = None):
        if cog is None:
            await ctx.send("Specify what to reload u dummy!")
            return
        await ctx.send(f"Reloading {cog}...") 
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Successfully reloaded {cog}")
        except ExtensionNotLoaded:
            await ctx.send(f"Umm so u havent even loaded {cog} yet x-x, ill try to load it")
            try:
                await self.bot.load_extension(f"cogs.{cog}")
                await ctx.send(f"Successfully loaded {cog}")
            except Exception as e:
                await ctx.send(f"Failed to load \"{cog}\": {e}")
        except Exception as e:
            await ctx.send(f"Failed to reload \"{cog}\": {e}")

    """
    Sync all / commands
    """
    @commands.command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx: Context):
        await ctx.send("Syncing...")
        synced = await self.bot.tree.sync()
        await ctx.send(f"Successfully synced {len(synced)} slash commands")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))