from discord.ext import commands
from discord.ext.commands import Cog
from cogs.data.dbIntegration import *
import random

class PrefixCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="setprefix", brief="Mengubah prefix bot ini di server kamu")
    @commands.has_permissions(ban_members=True)
    async def prefix(ctx, prefix : str):		
            if len(prefix) <= 4:
                if not any(c.isdigit() for c in prefix):
                    insert_prefix(ctx.guild.id, prefix)

                    await ctx.send(f"Prefix of this server has been changed to **{prefix}** successfully!")
                else:
                    await ctx.send("Integers are not allowed in prefixes")
            else:
                await ctx.send(f"A prefix must have only 4 or lesser charecters, **{len(prefix)}** is not allowed")

def setup(bot):
    bot.add_cog(PrefixCog(bot))