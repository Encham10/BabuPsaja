from logging import exception
from operator import truth
from sys import exc_info
from turtle import color
from typing import Optional
from unicodedata import name
from discord.ext import commands
from discord.ext.commands import Cog
from random import randrange

from cogs.data.dbIntegration import *
from cogs.data.console import *
import asyncio
import discord
import random

class TruthOrDareCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='truthordare', aliases=["tod"], brief ='Bermain truth or dare (dicommand ini ada sedikit bug)')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def truthordare(self, ctx, optional : Optional[str]):
        if optional == "help":
            embed=discord.Embed(
                title="<:info:955672054043115550> Truth Or Dare | Help",
                description="Beberapa command extension untuk >truth dan >dare",
                color=0xD4269A
            )
            embed.add_field(
                name=">dare",
                value="```\n>dare add\n>dare accept (owner bot only!)\n>dare id remove (owner bot only!)\n>dare delete (owner bot only!)\n```"
            )
            embed.add_field(
                name=">truth",
                value="```\n>truth add\n>truth accept (owner bot only!)\n>truth id remove (owner bot only!)\n>truth delete (owner bot only!)\n```"
            )
            await ctx.send(embed=embed)
        else:
            """Load Databases"""
            truths = random.choice(TruthData_list)
            dare = random.choice(DareData_list)
            """reply handler"""

            global times_used
            await ctx.send("**Truth Or Dare? [>truth/>dare]**\n```Coba gunakan [(>tod/>truthordare) + (help)]```")
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.content.lower() in [">truth", ">dare"]
                #Input Event
            msg = await self.bot.wait_for("message", check=check)
            if msg.content.lower() == ">truth":
                #Get a dare
                response = f"**{truths}**\n``15 Detik untuk menjawab!.``" 
                embed1= discord.Embed(title="✨ Truth!", description=response, color=discord.Color.blue())
                msg = await ctx.send(embed=embed1)
                #truth event here

                def check1(m):
                    return m.author.id == ctx.author.id

                newembed=discord.Embed(title="<:Done_:956133042412478524> Truth Terjawab!", description=response, color=discord.Color.green())
                newembed1=discord.Embed(title="<:Close_:956133042538283008> Truth Tidak Terjawab!", description=response, color=discord.Color.red())
                try:
                    await self.bot.wait_for('message', check=check1, timeout=15)
                    await msg.edit(embed=newembed)
                    return True
                except asyncio.TimeoutError: 
                    await msg.edit(embed=newembed1)
                    return False
                #Response Event
            else:
                if msg.content.lower() == ">dare":
                    #Get a dare
                    response = f"**{dare}**\n``35 Detik untuk menjawab!.``" 
                    embed=discord.Embed(title="✨ Dare!", description=response, color=discord.Color.blue())
                    msg = await ctx.send(embed=embed)
                    #Dare Event Here
                    def check(m):
                        return m.author.id == ctx.author.id

                    newembed3=discord.Embed(title="<:Done_:956133042412478524> Dare Terjawab!", description=response, color=discord.Color.green())
                    newembed4=discord.Embed(title="<:Close_:956133042538283008> Dare Tidak Terjawab!", description=response, color=discord.Color.red())
                    try:
                        await self.bot.wait_for('message', check=check, timeout=35)
                        await msg.edit(embed=newembed3)
                        return True
                    except asyncio.TimeoutError: 
                        await msg.edit(embed=newembed4)
                        return False
                else:
                    await ctx.send("jawab yang bener kocak! >truth/>dare")
            #Time Out Event
            times_used = times_used + 1
    
    @commands.command(name='dare', brief ='Menambahkan tantangan baru')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def dare(self, ctx, type, content : Optional[str]):
        if type == 'add':

            channelnotifer = self.bot.get_channel(940584110747947059)
            await ctx.send("Input Dare:")
            def check(m):
                return m.author.id == ctx.author.id

            message = await self.bot.wait_for('message', check=check)

            try:

                ForDBUpdate = str(message.content).capitalize()
                if ForDBUpdate[-4:] != ".":
                    ForDBUpdate = ForDBUpdate + "."

                RandomID = randrange(500)
                embed = discord.Embed(
                    title="New Dare",
                    description=f"<@{ctx.author.id}> Telah me-request tantangan baru",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="<:random:955682219781922896> Request ID:",
                    value=str(RandomID),
                    inline=False
                )
                embed.add_field(
                    name="<:add:955672054202507274> Tantangan:",
                    value=ForDBUpdate,
                    inline=False
                )
                InsertData_Dare(str(RandomID), ForDBUpdate)
                await ctx.send(embed=embed)
                await channelnotifer.send(embed=embed)

            except IOError:
                ConsoleERR(IOError)


            """Dare Delete"""
        elif type == 'delete':
            if ctx.author.id == 902406799351754812:

                await ctx.send("Input Dare: ")
                def check(m):
                    return m.author.id == ctx.author.id

                message = await self.bot.wait_for('message', check=check)
                if message.content in DareData:
                    content = message.content
                    x = str(DareData).replace(content, '')
                    UpdateData_Dare("6239a1be57cf9e4a1d86029c", x)
                    await ctx.send("Dare telah dihapus")              
                else:
                    await ctx.send("Dare tidak ditemukan")
                #embed = discord.Embed(
                 #   title="Delete Dare",
                  #  description=f"``{message}`` berhasil dihapus dari database.",
                   # color=discord.Color.red()
                #)

            """Dare Request Delete"""
        elif type == 'id':
            if content == 'remove':
                if ctx.author.id == 902406799351754812:

                    intruksi = await ctx.send("Input Dare ID: ")
                    def check(m):
                        return m.author.id == ctx.author.id

                    rawmessage = await self.bot.wait_for('message', check=check)
                    message = rawmessage.content
                    if CheckData(message) == True:
                        DeleteDataTOD(message)
                        embed = discord.Embed(
                            title="Request Dare Deleted",
                            description="Request Dare ID: " + message,
                            color=discord.Color.red()
                        )
                        await intruksi.delete()
                        await ctx.send(embed=embed)              
                    else:
                        await ctx.send("Request dare tidak ditemukan")
                    #embed = discord.Embed(
                    #   title="Delete Dare",
                    #  description=f"``{message}`` berhasil dihapus dari database.",
                    # color=discord.Color.red()
                    #)

            """Dare Request Accept"""
        elif type == 'accept':
            if ctx.author.id == 902406799351754812:
                intruksi = await ctx.send("Input Dare ID: ")
                def check(m):
                    return m.author.id == ctx.author.id

                rawmessage = await self.bot.wait_for('message', check=check)
                message = rawmessage.content
                if CheckData(message) == True:
                    embed = discord.Embed(
                        title="Request Dare Accepted",
                        description="Request Dare ID: " + message,
                        color=discord.Color.green()
                    )
                    UpdateAndDelete_Dare("6239a1be57cf9e4a1d86029c", message)
                    await intruksi.delete()
                    await ctx.send(embed=embed)         
                else:
                    await ctx.send("Request dare tidak ditemukan")
                #embed = discord.Embed(
                #   title="Delete Dare",
                #  description=f"``{message}`` berhasil dihapus dari database.",
                # color=discord.Color.red()
                #)

    @commands.command(name='truth', brief ='Menambahkan pertanyaan baru')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def truth(self, ctx, type, content : Optional[str]):
        if type == 'add':

            channelnotifer = self.bot.get_channel(940584110747947059)
            intruksi = await ctx.send("Input truth:")
            def check(m):
                return m.author.id == ctx.author.id

            message = await self.bot.wait_for('message', check=check)

            try:

                ForDBUpdate = str(message.content).capitalize()
                if ForDBUpdate[-4:] != "?":
                    ForDBUpdate = ForDBUpdate + "?"

                RandomID = randrange(500)
                embed = discord.Embed(
                    title="New Truth",
                    description=f"<@{ctx.author.id}> Telah me-request pertanyaan baru",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="<:random:955682219781922896> Request ID:",
                    value=str(RandomID),
                    inline=False
                )
                embed.add_field(
                    name="<:add:955672054202507274> Pertanyaan:",
                    value=ForDBUpdate,
                    inline=False
                )
                InsertData_Truth(str(RandomID), ForDBUpdate)
                await ctx.send(embed=embed)
                await channelnotifer.send(embed=embed)
                await intruksi.delete()

            except IOError:
                ConsoleERR(IOError)


            """Truth Delete"""
        elif type == 'delete':
            if ctx.author.id == 902406799351754812:

                await ctx.send("Input Truth: ")
                def check(m):
                    return m.author.id == ctx.author.id

                message = await self.bot.wait_for('message', check=check)
                if message.content in TruthData:
                    content = message.content
                    x = str(TruthData).replace(content, '')
                    UpdateData_Truth("6239a1be57cf9e4a1d86029c", x)
                    await ctx.send("Truth telah dihapus")              
                else:
                    await ctx.send("Truth tidak ditemukan")
                #embed = discord.Embed(
                 #   title="Delete ",
                  #  description=f"``{message}`` berhasil dihapus dari database.",
                   # color=discord.Color.red()
                #)

            """Truth Request Delete"""
        elif type == 'id':
            if content == 'remove' or 'delete':
                if ctx.author.id == 902406799351754812:

                    intruksi = await ctx.send("Input Truth ID: ")
                    def check(m):
                        return m.author.id == ctx.author.id

                    rawmessage = await self.bot.wait_for('message', check=check)
                    message = rawmessage.content
                    if CheckData(message) == True:
                        DeleteDataTOD(message)
                        embed = discord.Embed(
                            title="Request Truth Deleted",
                            description="Request Truth ID: " + message,
                            color=discord.Color.red()
                        )
                        await intruksi.delete()
                        await ctx.send(embed=embed)          
                    else:
                        await ctx.send("Request Truth tidak ditemukan")
                    #embed = discord.Embed(
                    #   title="Delete ",
                    #  description=f"``{message}`` berhasil dihapus dari database.",
                    # color=discord.Color.red()
                    #)

            """Truth Request Accept"""
        elif type == 'accept':
            if ctx.author.id == 902406799351754812:
                intruksi = await ctx.send("Input Truth ID: ")
                def check(m):
                    return m.author.id == ctx.author.id

                rawmessage = await self.bot.wait_for('message', check=check)
                message = rawmessage.content
                if CheckData(message) == True:
                    embed = discord.Embed(
                        title="Request Truth Accepted",
                        description="Request Truth ID: " + message,
                        color=discord.Color.green()
                    )
                    UpdateAndDelete_Truth("6239a1be57cf9e4a1d86029c", message)
                    await intruksi.delete()
                    await ctx.send(embed=embed)                 
                else:
                    await ctx.send("Request truth tidak ditemukan")
                #embed = discord.Embed(
                #   title="Delete ",
                #  description=f"``{message}`` berhasil dihapus dari database.",
                # color=discord.Color.red()
                #)


def setup(bot):
    bot.add_cog(TruthOrDareCog(bot))