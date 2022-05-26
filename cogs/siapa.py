from discord.ext import commands
from discord.ext.commands import Cog

import random

class SiapaCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='siapa', brief ='Memberi nama+tags secara acak')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def siapa(self, ctx, *, kalimat):
        if ctx.guild.id == 864789922233057300:
            """Check Room Request"""
            if ctx.channel.id == 950603060823064616:
                user = random.choice(ctx.guild.members)

                        # Just do it over if it is a bot
                while (user.bot):
                    user = random.choice(ctx.guild.members)
                Matches = ["gua", "aku", "gw", "saya", "sy", "sya"]
                if any (X in kalimat for X in Matches):
                    """Matches Handler"""
                    keterangan2 = None
                    if 'gua' in kalimat:
                        keterangan2 = kalimat.replace("gua", ctx.message.author.mention)
                    if 'gw' in kalimat:
                        keterangan2 = kalimat.replace("gw", ctx.message.author.mention)
                    if 'aku' in kalimat:
                        keterangan2 = kalimat.replace("aku", ctx.message.author.mention)
                    if 'saya' in kalimat:
                        keterangan2 = kalimat.replace("saya", ctx.message.author.mention)
                    if 'sya' in kalimat:
                        keterangan2 = kalimat.replace("sya", ctx.message.author.mention)
                    if 'sy' in kalimat:
                        keterangan2 = kalimat.replace("sy", ctx.message.author.mention)
                    """Close"""

                    await ctx.send("si " + user.mention + f" {keterangan2}")                    
                else:            
                    if 'yang' in kalimat:
                        await ctx.send("si " + user.mention + f" {kalimat}")
                    else:
                        await ctx.send("si " + user.mention + f" yang {kalimat}")
        else:
            user = random.choice(ctx.guild.members)

                    # Just do it over if it is a bot
            while (user.bot):
                user = random.choice(ctx.guild.members)
            Matches = ["gua", "aku", "gw", "saya", "sy", "sya"]
            if any (X in kalimat for X in Matches):
                """Matches Handler"""
                keterangan2 = None
                if 'gua' in kalimat:
                    keterangan2 = kalimat.replace("gua", ctx.message.author.mention)
                if 'gw' in kalimat:
                    keterangan2 = kalimat.replace("gw", ctx.message.author.mention)
                if 'aku' in kalimat:
                    keterangan2 = kalimat.replace("aku", ctx.message.author.mention)
                if 'saya' in kalimat:
                    keterangan2 = kalimat.replace("saya", ctx.message.author.mention)
                if 'sya' in kalimat:
                    keterangan2 = kalimat.replace("sya", ctx.message.author.mention)
                if 'sy' in kalimat:
                    keterangan2 = kalimat.replace("sy", ctx.message.author.mention)
                """Close"""

                await ctx.send("si " + user.mention + f" {keterangan2}")                    
            else:               
                if 'yang' in kalimat:
                    await ctx.send("si " + user.mention + f" {kalimat}")
                else:
                    await ctx.send("si " + user.mention + f" yang {kalimat}")

def setup(bot):
    bot.add_cog(SiapaCog(bot))