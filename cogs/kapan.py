from discord.ext import commands
from discord.ext.commands import Cog

import random

class KapanCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='kapan', aliases=["kpn"], brief ='Menanyakan kapan akan terjadi(Tidak Serius)')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def kapan(self, ctx, *, kalimat):
        """Check Guild Id"""
        if ctx.guild.id == 864789922233057300:
            """Check Room Request"""
            if ctx.channel.id == 950603060823064616:
                randomchoise = ["ga tau", "nanti", "mungkin 4 bulan", "kurang tau", "emang bakalan jadi?", "bulan depan", "bentar lagi", "taun depan", "minggu ini", "dibulan ini", "gtw"]
                if (ctx.message.content in [">kapan-kapan", ">kapan aja", ">kapan kapan", ">kapan", ">kapan aku", "kapan doang"]):
                    randomchoise1 = ["ga jelas", "kapan apaan kanjut", "kapan apanya", "yang bener anjime", "lluwh gjls"]
                    await ctx.send(f"{random.choice(randomchoise1)}")
                else:
                    await ctx.send(f"{random.choice(randomchoise)}")             
        else:
                randomchoise = ["ga tau", "nanti", "mungkin 4 bulan", "kurang tau", "emang bakalan jadi?", "bulan depan", "bentar lagi", "taun depan", "minggu ini", "dibulan ini", "gtw"]
                if (ctx.message.content in [">kapan-kapan", ">kapan aja", ">kapan kapan", ">kapan", ">kapan aku", "kapan doang"]):
                    randomchoise1 = ["ga jelas", "kapan apaan kanjut", "kapan apanya", "yang bener anjime", "lluwh gjls"]
                    await ctx.send(f"{random.choice(randomchoise1)}")
                else:
                    await ctx.send(f"{random.choice(randomchoise)}")

def setup(bot):
    bot.add_cog(KapanCog(bot))