from discord.ext import commands
from discord.ext.commands import Cog

class QuickvoteCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='poll', aliases=['vote', 'voting', 'polling', 'quickvote'], brief ='Membuat polling atau vote cepat')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def poll(self, ctx, *, keterangan):
        question2 = None

        """Matches Handler"""
        question2 = keterangan
        if 'gua' in keterangan:
            question2 = keterangan.replace("gua", ctx.message.author.mention)
        if 'gw' in keterangan:
            question2 = keterangan.replace("gw", ctx.message.author.mention)
        if 'aku' in keterangan:
            question2 = keterangan.replace("aku", ctx.message.author.mention)
        if 'saya' in keterangan:
            question2 = keterangan.replace("saya", ctx.message.author.mention)
        if 'sya' in keterangan:
            question2 = keterangan.replace("sya", ctx.message.author.mention)
        if 'sy' in keterangan:
            question2 = keterangan.replace("sy", ctx.message.author.mention)
            """Close"""
        message = await ctx.send(f"POLL!✅❎\n**{question2}**")        
        await message.add_reaction('❎')        
        await message.add_reaction('✅')     

def setup(bot):
    bot.add_cog(QuickvoteCog(bot))