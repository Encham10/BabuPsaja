from discord.ext import commands
from discord.ext.commands import Cog

import discord
import os

"""Too Lazy"""
from cogs.data.dbIntegration import *
from pymongo import MongoClient

def validate(date_text):
        date_text = '2020/'+ date_text
        try:
            datetime.strptime(date_text, '%Y/%m/%d')
            return True
        except ValueError:
            return False

class BrithdayCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name='birthday')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def birthday(self, ctx):
        Server_Prefix = None
        try:
            Server_Prefix = fetch_prefix(ctx.guild.id)["prefix"]
        except:
            Server_Prefix = ">"
            pass
        embed = discord.Embed(
                title ='Help with Birthday',
                color = 0xD4269A
            )
        embed.add_field(name=f'{Server_Prefix}add name mm/dd', value='Add a name and birthday to the system.', inline=False)
        embed.add_field(name=f'{Server_Prefix}all', value='Lists all birthdays in the system.', inline=False)
        embed.add_field(name=f'{Server_Prefix}delete name', value='Removes a birthday from the system.', inline=False)
        embed.add_field(name=f'{Server_Prefix}deleteAll', value='Removes all birthday\'s added.Administrator\'s only', inline=False)
        embed.add_field(name=f'{Server_Prefix}edit name', value='Allows you to edit a birthday in the system with that corresponding name.', inline=False)
        embed.add_field(name=f'{Server_Prefix}help', value='Lists all bot commands.', inline=False)
        embed.add_field(name=f'{Server_Prefix}here', value='Allocates all Happy birthday notices to current channel.', inline=False)
        embed.add_field(name=f'{Server_Prefix}month monthoftheyear', value='Allows you to view all birthdays for that month.', inline=False)
        embed.add_field(name=f'{Server_Prefix}name username', value='Shows birthdate of user if in the system', inline=False)
        embed.add_field(name=f'{Server_Prefix}thisMonth', value='Shows all birthdays for the current month.', inline=False)
        embed.add_field(name=f'{Server_Prefix}today', value='Prints a happy birthday message for birthdays today', inline=False)
        await ctx.send(embed=embed)

    """Main Commands"""
    @commands.command(name='all')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def all(self, ctx):
        msg = ''
        for birthday in birthdays.find({"sid":ctx.guild.id}).sort('birthday',1):
            name = birthday["name"]
            msg = msg + name + ' ' + birthday['birthday'] + '\n'
        if not msg:
            await ctx.send("No birthdays have been added yet")
        else:    
            await ctx.send(msg)

    @commands.command(name='today')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def today(self, ctx):
        date = datetime.date(datetime.now())
        datem = date.strftime('%y/%m/%d')
        results = birthdays.find({"birthday":datem[3:], "sid":ctx.guild.id})
        if results.count() < 1:
            msg = 'No birthdays today'
            await ctx.send(msg)
        else:
            for birthday in results:
                name = birthday["name"]
                await ctx.send('Happy Birthday, %s!' % name)

    @commands.command(name='thismonth')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def thisMonth(self, ctx):
        date = datetime.date(datetime.now())
        datem = date.strftime('%y/%m/%d')
        month = str(datem[3:5])
        
        results = birthdays.find({"month":month, "sid":ctx.guild.id}).sort('birthday',1)
        if results.count() < 1:
            msg = 'No birthdays this month'
            await ctx.send(msg)
        else:
            msg = ''
            for birthday in results:
                name = birthday["name"]
                msg = msg + name + ' ' + birthday['birthday'] + '\n'
            await ctx.send(msg)

    @commands.command(name='month')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def month(self, ctx, month):
        month = month.lower()
        months = dict(january='01',february='02', march='03', april='04', may='05', june='06', july='07', august='08', september='09',october='10',november='11',december='12')
        results = birthdays.find({"month":months[month], "sid":ctx.guild.id}).sort('birthday',1)
        if results.count() < 1:
            msg = 'No birthdays in %s' % month
            await ctx.send(msg)
        else:
            msg = ''
            for birthday in results:
                    name = birthday["name"]
                    msg = msg + name + ' ' + birthday['birthday'] + '\n'
            await ctx.send(msg)

    @commands.command(name='name')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def name(self, ctx, name):
        results = birthdays.find({"name":name, "sid":ctx.guild.id})
        if results.count() < 1:
            msg = 'No birthdays found with that name'
            await ctx.send(msg)
        else:
            for birthday in results:
                await ctx.send(birthday["birthday"])

    def validate(date_text):
            date_text = '2020/'+ date_text
            try:
                datetime.strptime(date_text, '%Y/%m/%d')
                return True
            except ValueError:
                return False

    @commands.command(name='add')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def add(self, ctx, name, birthday):
        if len(birthday) < 4:
            return False
        # make sure birthday is listed in the right format
        if validate(birthday) == False:
            await ctx.send("Incorrect data format, should be MM/DD")
        else:
            results = birthdays.find_one({"sid":ctx.guild.id})
            if db.collection.count_documents({ 'sid': ctx.guild.id }, limit = 1) != 0:
                results = birthdays.find_one({"sid":ctx.guild.id})
                birthdays.insert_one({
                    "name": name,
                    "birthday": birthday,
                    "month": birthday[:2],
                    "sid": ctx.guild.id,
                    "cid": str(results["cid"])
                    })
                await ctx.send(name + '\'s birthday was added')
            else:
                await ctx.send('Suruh moderator server mu untuk set channel terlebih dahulu >here')

    @commands.command(name='delete')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def delete(self, ctx, name):
        results = birthdays.find({"name":name, "sid":ctx.guild.id})
        if results.count() < 1:
                msg = 'No birthdays found with that name'
                await ctx.send(msg)
        else:
            birthdays.delete_one({"name":name, "sid":ctx.guild.id})
            await ctx.send('Birthday deleted')

    @commands.command(name='deleteall')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def deleteAll(self, ctx):
        #send a message to confirm
        await ctx.send('Are you sure you want to delete all birthdays? Enter y for yes or n for no')
        #pull in response
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
        if msg.content == 'n':
            await ctx.send('No worries nothing was deleted')
        elif msg.content == 'y':
                # set up a role check
                if ctx.message.author.guild_permissions.administrator:
                    birthdays.delete_many({"sid":ctx.guild.id})
                    await ctx.send('All Birthday\'s have been deleted')
                else: 
                    await ctx.send('Only Administrators can use this function')
        else:
            await ctx.send('Operation ended. Invalid input')

    @commands.command(name='edit')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def edit(self, ctx, name, birth):
        results = birthdays.find({"name":name, "sid":ctx.guild.id})
        if results.count() < 1:
            msg = 'No birthdays found with that name'
            await ctx.send(msg)
        elif validate(birth) == False:
            await ctx.send("Incorrect data format, should be MM/DD")
        else: 
            birthdays.update_one({"name":name, "sid":ctx.guild.id}, {"$set":{"birthday":birth, "month":birth[:2]}})
            await ctx.send('Birthday updated')

    @commands.command(name='here')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def here(self, ctx):
        await ctx.send('Are you sure you want all birthday messages posted here? Enter yes or no')
        #pull in response
        msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
        if msg.content == 'no':
            await ctx.send('No worries nothing was changed')
        elif msg.content == 'yes':
            # set up a role check
            if ctx.message.author.guild_permissions.administrator:
                birthdays.update_many({"sid":ctx.guild.id}, {"$set":{"cid": ctx.channel.id}})
                await ctx.send('All Birthday notices will appear here')
            else:
                await ctx.send('Only Administrators can use this function')
        else:
            await ctx.send('Operation ended. Invalid input')

def setup(bot):
    bot.add_cog(BrithdayCog(bot))