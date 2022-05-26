from discord.ext import commands
from discord.ext.commands import Cog

import discord
import random
import json
import os

"""Load JSON"""
cwd = os.getcwd()
with open(cwd + "/cogs/data/configs.json") as data_file:    
    configs = json.load(data_file)

class EventCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def on_message(self, ctx):
        randomchoise = ["sok dingin kanjut", "dingin cuy dingin", "dingin amat", "berusaha menjadi dingin"]
        if(ctx.content  == "pagi"):
            await ctx.channel.send(configs["pagi"])
        if(ctx.content  == "sore"):
            await ctx.channel.send(configs["sore"])        
        if(ctx.content  == "malam"):
            await ctx.channel.send(configs["malam"])

        if(ctx.content.lower() in ["ok","sip","Ok","Sip","o","O","👍", "y", "y.", "k", "k.", "o.", "g", "g.", "ogt.", "ogt", "pnsi", "pnsi."]):
            await ctx.channel.send(random.choice(randomchoise), reference=ctx)

        if(ctx.content == "sange sama kartun"):
            await ctx.channel.send("https://cdn.discordapp.com/attachments/880509666482860042/884722248303403008/video0-18.mp4", reference=ctx)

def setup(bot):
    bot.add_cog(EventCog(bot))