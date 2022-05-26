from discord.ext import commands
from discord.ext.commands import Cog

import random

class ApakahCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='apakah', brief ='Menanyakan apakah [kalimat] benar atau tidak(tidak serius)')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def apakah(self, ctx, *, kalimat):
        """Check Guild Id"""
        if ctx.guild.id == 864789922233057300:
            """Check Room Request"""
            if ctx.channel.id == 950603060823064616:
                randomchoise = ["kayaknya iya", "ga", "ga tau", "enggak juga", "kurang tau", "kurang yakin", "bisa jadi", "mungkin aja", "iya kayaknya", "bisa dibilang iya", "kata siapa?", "fek", "ril", "engga lah", "ngga kayaknya", "ga mungkin"]
                if (ctx.message.content in [">apakah bot aja", ">apakah iya", ">apakah", ">apakah aku", "apakah doang", ">apakah akan"]):
                    randomchoise1 = ["ga jelas", "apakah apaan kanjut", "apakah apanya", "yang bener anjime", "lluwh gjls"]
                    await ctx.send(f"{random.choice(randomchoise1)}")
                else:
                    await ctx.send(f"{random.choice(randomchoise)}")
        else:
                randomchoise = ["kayaknya iya", "ga", "ga tau", "enggak juga", "kurang tau", "kurang yakin", "bisa jadi", "mungkin aja", "iya kayaknya", "bisa dibilang iya", "kata siapa?", "fek", "ril", "engga lah", "ngga kayaknya", "ga mungkin"]
                if (ctx.message.content in [">apakah bot aja", ">apakah iya", ">apakah", ">apakah aku", "apakah doang", ">apakah akan"]):
                    randomchoise1 = ["ga jelas", "apakah apaan kanjut", "apakah apanya", "yang bener anjime", "lluwh gjls"]
                    await ctx.send(f"{random.choice(randomchoise1)}")
                else:
                    await ctx.send(f"{random.choice(randomchoise)}")

def setup(bot):
    bot.add_cog(ApakahCog(bot))