import package
package.setup()

import asyncio

import discord
from random import randrange
from discord.ext import commands, tasks
import pyppeteer

from config import config
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings

initial_extensions = ['musicbot.commands.music',
                      'musicbot.commands.general', 'musicbot.plugins.button']

from cogs.data.console import *
from cogs.data.dbIntegration import *
from cogs.radio import *
client = commands.Bot(command_prefix=get_prefix, intents = discord.Intents.all(), case_insensitive=True)
client.remove_command("help")

#TASK ====>
async def activity_task():
    while True:
        await client.change_presence(activity=discord.Game(name="MAINTAINCE"), status=discord.Status.idle)
        await asyncio.sleep(6)
        await client.change_presence(activity=discord.Game(name="DJAINURI ♡"), status=discord.Status.idle)
        await asyncio.sleep(6)
        await client.change_presence(activity=discord.Game(name="♡ RANGGA"), status=discord.Status.idle)
        await asyncio.sleep(6)

@tasks.loop(hours=1)
async def called_once_a_hour():
    await client.wait_until_ready()
    date = datetime.date(datetime.now())
    datem = date.strftime('%y/%m/%d')
    results = birthdays.find({"birthday":datem[3:]})
    for birthday in results:
        name = birthday["name"]
        channel = client.get_channel(birthday["cid"])
        msg = '@everyone\nHappy Birthday, %s! have a nice birthday 🎂🎉' % name
        print(msg)
        await channel.send(msg)

#COGS ====>
async def load_extensions():
    modules = [
    'apakah', 
    'coldown_handler', 
    'event',
    'help',
    'kapan',
    'quickvote',
    'saran',
    'siapa',
    'truthordare',
    'utility',
    'tiktok',
    'ben',
    'birthday',
    'prefix'# 21 Mei 2022
    ]
    try:
        for module in modules:
            client.load_extension('cogs.' + module)
            Console("BOT", f"Loaded cog {module}")
        for extension in initial_extensions:
            client.load_extension(extension)
            Console("BOT", f"Loaded cog {extension}")
    except Exception as e:
        ConsoleERR(f'Error loading {module}: {e}')

async def register(guild):

    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(client, guild)

    sett = guild_to_settings[guild]

    try:
        await guild.me.edit(nick=sett.get('default_nickname'))
    except:
        pass

    if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
        return

    vc_channels = guild.voice_channels

    if sett.get('vc_timeout') == False:
        if sett.get('start_voice_channel') == None:
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)

        else:
            for vc in vc_channels:
                if vc.id == sett.get('start_voice_channel'):
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)


def getGuildName(n):
    return [n.name, n.member_count]
    
def getNum(obj):
    return obj[1]

#====START ====>


#EVENTS====>   
if __name__ == '__main__': 
    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit

    Console("MUSIC", "MUSICBOT Loaded")
    Console("MUSIC", "https://github.com/mytja/harmonoid-music-bot")

    @client.event
    async def on_guild_join(guild):
        print(guild.name)
        await register(guild)

    Console_Sepator()
    @client.event
    async def on_ready():
        await load_extensions()
        await client.change_presence(activity=discord.Game(name="MAINTAINCE"), status=discord.Status.idle)
        Console_Sepator()
        Console("BOT", f"Logged in as {client.user.name}")
        Console("BOT", f"Logged in as {client.user.id}")
        Console_Sepator()
        guildsSm =list(map(getGuildName, client.guilds))
        
        guildsSm.sort(key=getNum)
        Console("BOT", f"{guildsSm}")
        totalusers = 0
        for i in guildsSm:
            totalusers += i[1]
        # print("discords using bot: " + str(db["discordsUsingBot"]))
        # print("Total discords using bot " + str(len(db["discordsUsingBot"])))
        # # db["listOfDiscordsMess"] = []
        # # toMake = []
        # # for i in range(0, len(db["discordsUsingBot"])):
        # #     toMake.append(0)
        # # print(toMake)
        # db["listOfDiscordsMess"] = toMake
        # print(db["listOfDiscordsMess"])
        """MusicCogs"""
        for guild in client.guilds:
            await register(guild)
            print("Joined {}".format(guild.name))

        print(config.STARTUP_COMPLETE_MESSAGE)

        try:
            channel = client.get_channel(957973963789729863)
            guild = client.get_guild(864789922233057300)
            client.loop.create_task(called_once_a_hour())
        except AttributeError:
            await print('User is not in accessible voice channel!')
        #await radio("mustang-fm", channel=channel, guild=guild)

    import uptimer

    uptimer.awake("https://tiktok-auto-embed.encham.repl.co/", False)
    TOKEN = os.environ['TOKEN']
    try:
        client.run(TOKEN, reconnect=True)
    except:
        os.system("kill 1")
        client.run(TOKEN, reconnect=True)