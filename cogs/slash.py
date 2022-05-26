from discord.ext import commands
from discord.ext.commands import Cog

import random

class SlashCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    """Coming Fuckin Soon"""
    
def setup(bot):
    bot.add_cog(SlashCog(bot))