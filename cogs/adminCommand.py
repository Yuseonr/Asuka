from discord.ext import commands
from discord.ext.commands import Context, ExtensionNotLoaded
import os
import sys
import importlib

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
    Reload Service {currently only simple_ai} reload all file in folder of the spesified service
    """
    @commands.command(name="reload_service")
    @commands.is_owner()
    async def reload_service(self, ctx: Context, service: str = None):
        if service is None:
            await ctx.send("Specify what service to reload u dummy!")
            return
        
        physical_path = f"./services/{service}"
        if not os.path.isdir(physical_path):
            await ctx.send(f"Are you blind? The folder `{physical_path}` doesn't even exist on the hard drive, yus.")
            return

        reloaded_files = []
        errors = []

        for filename in os.listdir(physical_path):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                full_module_path = f"services.{service}.{module_name}"

                try:
                    if full_module_path in sys.modules:
                        importlib.reload(sys.modules[full_module_path])
                        reloaded_files.append(module_name)
                    else:
                        importlib.import_module(full_module_path)
                        reloaded_files.append(f"{module_name} (New)")
                        
                except Exception as e:
                    errors.append(f"{module_name}: {e}")

        if errors:
            error_text = "\n".join(errors)
            await ctx.send(f"Hmph. I tried to reload `{physical_path}`, but your code is completely broken:\n```py\n{error_text}\n```")
        elif not reloaded_files:
            await ctx.send(f"I checked `{physical_path}`, but there were no valid Python files in there to reload.")
        else:
            success_text = ", ".join(reloaded_files)
            await ctx.send(f"Successfully hot-reloaded `{physical_path}`:\n`[{success_text}]`\nTry not to break it again, yus.")


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