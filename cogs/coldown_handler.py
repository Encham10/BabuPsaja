from discord.ext import commands
from discord.ext.commands import Cog

from cogs.data.console import *

import random

class ColdownCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """Coldown Handler"""
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            randomchoise10 = ["slow dikit", "bentar", "bentaran jangan dispam", "stop dulu", "bentar cayang ku"]
            await ctx.send(f"{random.choice(randomchoise10)}, tunggu {round(error.retry_after, 2)} detik lagi!")
        elif isinstance(error, commands.MissingRequiredArgument):
            ConsoleERR("Missing required arguments. Please type in *all* arguments.")    
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the necessary permissions.")

def setup(bot):
    bot.add_cog(ColdownCog(bot))