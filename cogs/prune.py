from logging import exception
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

from cogs.data.dbIntegration import *

import random
import discord

class Buttons(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()
    @discord.ui.button(label="Member List",style=discord.ButtonStyle.gray)
    async def MemberList(self, button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.send_message(content=f"{self.bot.get_all_members()}", ephemeral=True)
    @discord.ui.button(label="Verified Member List",style=discord.ButtonStyle.gray)
    async def VerifiedMemberList(self, button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.send_message(content=f"{GetMemberList()}", ephemeral=True)
    @discord.ui.button(label="Close Session",style=discord.ButtonStyle.red)
    async def CloseSession(self, button:discord.ui.Button,interaction:discord.Interaction):
        CloseSession()
        await interaction.response.send_message(content="Done!", ephemeral=True)

class PruneCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context. 
    
    @commands.command(name='prune', pass_context=True, brief ='Psaja Prune Member')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def prune(self, ctx):
        if ctx.author.id == 902406799351754812:
            Console("Prune", "Pruning")
            OpenSession()
            Console("Prune", "Open Session")
            embed = discord.Embed(
                title="<:info:955672054043115550> Psaja Prune Member",
                description="Pengurangan member untuk inactive user\nPengurangan member dilakukan 1 bulan sekali\nKetik >verify untuk verifikasi kalo akun kamu masih aktif.",
                color=0xD4269A
            )
            Console("Prune", "Sending Embed")
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send("test")
                except:
                    pass
            await ctx.send("Done!", view=Buttons)

    @commands.command(name='Verify', pass_context=True, brief ='Psaja Prune Member')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def verify(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            #Cek apakah sesi masih dibuka
            if GetExpired() == "False":
                if IfMemberExist(ctx.author) == False:
                    await ctx.send("<:Done_:956133042412478524> Kamu sudah terverify!")  
                    #Mengirim user data
                    InsertMember(ctx.author)      
            elif GetExpired() == "False":
                await ctx.send("<:Close_:956133042538283008> Sesi Verify sudah berakhir. DM Encham#0008 bila ada keperluan")
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(PruneCog(bot))