from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

import random

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='hide', pass_context=True, brief ='[Psaja]  Memberi role khusus untuk hide/unhide room')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def hide(self, ctx, *, room):
        """Check If Psaja"""
        if ctx.guild.id == 864789922233057300:
            """Check Room Request"""
            if ctx.channel.id == 950603060823064616:
                member = ctx.message.author
                randomchoise = ["kamu di-hide", "kamu ter-hide", "kamu berhasil di-hide sesuai request", "udah", "udah coba cek"]
                if room == "general":
                    """General"""
                    role = get(member.guild.roles, name="❀ General                        ⁣                            ⁣")
                    await member.add_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "roleroom":
                    """Role Room"""
                    role = get(member.guild.roles, name="❀ Role Room                          ⁣                            ⁣")
                    await member.add_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "bot":
                    """BotRequest Role"""
                    role = get(member.guild.roles, name="❀ Bot Request                            ⁣                            ⁣")
                    await member.add_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "meme":
                    """Shitpost Role"""
                    role = get(member.guild.roles, name="❀ Shitpost                            ⁣                            ⁣")
                    await member.add_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")


    @commands.command(name='unhide', pass_context=True, brief ='[Psaja]  Mencopot role khusus untuk hide/unhide room')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def unhide(self, ctx, *, room):
        """Check If Psaja"""
        if ctx.guild.id == 864789922233057300:
            """Check Room Request"""
            if ctx.channel.id == 950603060823064616:
                member = ctx.message.author
                randomchoise = ["kamu di-unhide", "kamu ter-unhide", "kamu berhasil di-unhide sesuai request", "udah", "udah coba cek"]
                if room == "general":
                    """General"""
                    role = get(member.guild.roles, name="❀ General                        ⁣                            ⁣")
                    await member.remove_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "roleroom":
                    """Role Room"""
                    role = get(member.guild.roles, name="❀ Role Room                          ⁣                            ⁣")
                    await member.remove_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "bot":
                    """BotRequest Role"""
                    role = get(member.guild.roles, name="❀ Bot Request                            ⁣                            ⁣")
                    await member.remove_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")
                if room == "meme":
                    """Shitpost Role"""
                    role = get(member.guild.roles, name="❀ Shitpost                            ⁣                            ⁣")
                    await member.remove_roles(role)
                    await ctx.send(f"{random.choice(randomchoise)}")

def setup(bot):
    bot.add_cog(UtilityCog(bot))