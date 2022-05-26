from discord.ext import commands
from discord.ext.commands import Cog
from discord import Webhook

import discord
import aiohttp

class SaranCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='Saran', pass_context=True, description="Saran atau tambahan harus jelas sehingga staff mengerti, jika tidak sesuai format/tidak jelas, maka admin berhak menghapus atau menolak saran/tambahan.")
    @commands.cooldown(1, 3600, commands.BucketType.guild)
    async def saran(self, ctx, *, keterangan):
        channelnotifer = self.bot.get_channel(956105062051110932)
        embed = discord.Embed(title="Saran! ✨", description=f"👋 **{ctx.author.name}#{ctx.author.discriminator}**\n{keterangan}") # Initializing an Embed
        await ctx.send("Pesan mu telah dikirim! *saranmu akan segera direalisasikan* ``(kanjut yang ngespam saran, commandnya tak kasih coldown 1 jam)``")
        await channelnotifer.send(embed=embed)

def setup(bot):
    bot.add_cog(SaranCog(bot))