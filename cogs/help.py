from turtle import color, title
from unicodedata import name

from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

import discord
import os

from cogs.data.dbIntegration import *
from typing import Optional

def syntax(command):
	cmd_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)

	return f"`{cmd_and_aliases} {params}`"

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Fun Commands",emoji="<:fun:955682219689672784>",description="Menunjukan beberapa perintah gokil!"),
            discord.SelectOption(label="Random Commands",emoji="<:random:955682219781922896>",description="Opsi ini akan menunjukan perintah-perintah Random"),
            discord.SelectOption(label="Utility",emoji="<:settings:955682219685462056>",description="Diopsi ini ada beberapa perintah yang hanya bisa digunakan di Psaja")
            ]
        super().__init__(placeholder="Pilih Command..",max_values=1,min_values=1,options=options)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="You took too long! Disabled all the components.", view=self)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Fun Commands":
            newembed_fun = discord.Embed(
            title="\n<:fun:955682219689672784> Fun Commands:", 
            description="``Jalankan >help <command> untuk melihat info Command tersebut.\n``\n**Command List:**```\nsiapa,  kapan,  apakah,  truthordare```",
            color=0xD4269A
            )
            await interaction.response.edit_message(embed=newembed_fun)
        elif self.values[0] == "Random Commands":
            newembed_randomcmd = discord.Embed(
            title="\n<:random:955682219781922896> Random Commands:", 
            description="``List Command disini ga bisa dipakai di >help <command>.\n``\n**Command List:**```\npagi,  sore,  malam,  sange sama kartun```",
            color=0xD4269A
            )
            await interaction.response.edit_message(embed=newembed_randomcmd)
        elif self.values[0] == "Utility":
            newembed_utilitycmd = discord.Embed(
            title="\n<:settings:955682219685462056> Utility:", 
            description="``Jalankan >help <command> untuk melihat info Command tersebut.\n``\n**Commmand List:**```\nhide/unhide,  poll,  saran,  setprefix,  >birthday```",
            color=0xD4269A
            )   
            await interaction.response.edit_message(embed=newembed_utilitycmd)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class HelpCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cmd_help(self, ctx, command):
        embed = discord.Embed(title=f"<:info:955672054043115550> Help with `{command}`",
                      description=syntax(command),
                      color=0xD4269A)
        embed.add_field(name="Command description:", value=command.brief)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx,  cmd: Optional[str]):
        Server_Prefix = None
        try:
            Server_Prefix = fetch_prefix(ctx.guild.id)["prefix"]
        except:
            Server_Prefix = ">"
            pass
        if not cmd:
            embed = discord.Embed(
                title="\n<:add:955672054202507274> Invite:", 
                description="**Mau invite bot ini ke server kamu?** Pencet ini [Invite Me!](https://discord.com/oauth2/authorize?client_id=903613536159281253&scope=bot&permissions=8) pastikan kamu sudah login di browser kamu!",
                color=0xD4269A
            )
            embed.add_field(
                name="<:info:955672054043115550> Bot Info:",
                value=f"Server prefix ku adalah **{Server_Prefix}**\nPilih *command* yang ingin kamu ketahui, pilih *dibawah* pesan ini",
                inline=False
            )
            embed.add_field(
                name="<:robot:955683431663140878> Command Categories:",
                value="<:fun:955682219689672784> - ``Fun Commands``\n<:random:955682219781922896> - ``Random Commands``\n<:settings:955682219685462056> - ``Utility``",
                inline=False
            )
            embed.set_footer(
                text="BabuPsaja"
            )
            await ctx.send(embed=embed, view=SelectView())

        else:
            if (command := get(self.bot.commands, name=cmd)):
                    await self.cmd_help(ctx, command)
            else:
                    await ctx.send("Ga nemu commandnya, coba cek lagi")


        

def setup(bot):
    bot.add_cog(HelpCog(bot))