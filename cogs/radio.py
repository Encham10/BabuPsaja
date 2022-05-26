from discord.ext import commands
from discord.ext.commands import Cog

import pyppeteer
import discord

async def AccessPlaylist(url):
    print("Starting process")
    browser = await pyppeteer.launch({
        'headless': True,
        "args": ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36')
    # await page.setDefaultNavigationTimeout(1000000)
    await page.goto(url, {"waitUntil": 'load', "timeout": 1000000})
    await browser.close()

async def radio(stasiun : str, channel : discord.VoiceChannel, guild : discord.guild):

    #For Mustang-FM

    voice_client = None
    try:
        voice_client = await channel.connect()
    except:
        print("Bot already in a channel")

    #Radio source
    radiosource_MusstangFM = 'https://wz.mari.co.id:1936/web_mustangfm/mustangfm/playlist.m3u8'
    radiosource_Prambors = 'https://playerservices.streamtheworld.com/api/livestream-redirect/PRAMBORS_FMAAC.aac?dist=onlineradiobox'
    radiosource_KissFM = 'https://wz.mari.co.id:1936/web_kisfm/kisfm/playlist.m3u8'
    if stasiun.lower() == "mustang-fm":
        try:
            await AccessPlaylist("https://mustang88fm.com/streaming")
            mustangfm = discord.FFmpegOpusAudio(source=radiosource_MusstangFM)
            voice_client.play(mustangfm)
        except:
            print("Access to playlist failed")
    
    elif stasiun.lower() == "prambors":
        pramborsfm = discord.FFmpegOpusAudio(source=radiosource_Prambors)
        voice_client.play(pramborsfm)

    elif stasiun.lower() == "kis-fm":
        try:
            await AccessPlaylist("https://kis951fm.com/streaming")
            mustangfm = discord.FFmpegOpusAudio(source=radiosource_MusstangFM)
            voice_client.play(mustangfm)
        except:
            print("Access to playlist failed")
        kissfm = discord.FFmpegOpusAudio(source=radiosource_KissFM)
        voice_client.play(kissfm)

    await guild.change_voice_state(channel=channel, self_deaf=True)

class RadioCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()  # this is now required in this context. 

    @commands.command(name="play", brief="Memainkan stasiun radio (mustang-fm, prambors, kis-fm)")
    async def play(self, ctx, *, stasiun):
        try:
            await ctx.guild.voice_client.disconnect()
        except:
            print("Bot already disconect")

        try:
            channel = self.bot.get_channel(957973963789729863)
            guild = self.bot.get_guild(864789922233057300)
        except AttributeError:
            await print('User is not in accessible voice channel!')

        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send('User is not in accessible voice channel!')

        if stasiun.lower() == "prambors":
            await radio("prambors", channel=channel, guild=guild)
            await ctx.send("Memainkan Prambors")

        if stasiun.lower() == "mustang-fm":
            await radio("mustang-fm", channel=channel, guild=guild)
            await ctx.send("Memainkan Mustang-FM")

        if stasiun.lower() == "kis-fm":
            await radio("kis-fm", channel=channel, guild=guild)
            await ctx.send("Memainkan KisFM")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RadioCog(bot), guilds=[discord.Object(id=864789922233057300)])