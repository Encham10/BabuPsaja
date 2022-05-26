from click import option
from discord.ext.commands import Cog
from discord.ext import commands

import os
import asyncio
from random import choice
from random import randrange

import discord
from discord import Webhook

from cogs.data.dbIntegration import *

"""Import MongoDB"""
#For Repl It
#cluster = MongoClient(os.getenv("DATABASE_CLIENT_URL"))
#

"""List To STR"""
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1      

class BenCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

 

    """Check If Member Disconect"""
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """User DataDB"""
        guild = member.guild
        try:
            dataDB =  Ben_FindGuild(guild.id)
            channel = self.bot.get_channel(dataDB["channelid"])
            if dataDB["memberid"] is not None:
                if not after.channel and before.channel and member.id == dataDB["memberid"]:
                    await channel.send(f"<:ben:955393615897694228>:\n*Ended call with* <@{member.id}>")
                    """Delete Document"""
                    Ben_Delete(dataDB)
                    await member.guild.voice_client.disconnect()
                    return True
        except:
            return False

    """Ben call and Question Event: """
    @commands.Cog.listener()
    async def on_message(self, message):
        cmd = str(message.content).lower()
        guild = message.guild.id
        voice_client = None
        voice_client2 = None
        cwd = os.getcwd()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        if "ben call" in cmd:
            if message.guild.id == '864789922233057300':
                return message.channel.send("[INFO] Ben sudah tidak tersedia untuk layanan diserver ini.")
            elif Ben_Exist("guildid", guild) == False:
                #if doesnt exist Return:
                """Voice Client"""
                try:
                    channel = message.author.voice.channel
                except AttributeError:
                    await message.channel.send('User is not in accessible voice channel!')
                if voice_client:
                    await voice_client.disconnect()

                """FFMPEG"""
                try:
                    voice_client = await channel.connect()
                    audio_source = await discord.FFmpegOpusAudio.from_probe(source=f'{cwd}/cogs/data/Ben.mp3')
                    voice_client.play(audio_source)
                except:
                    pass

                """Main Core"""
                """Create Webhook"""
                await message.channel.send('<:ben:955393615897694228>:\n*Ring*.. Ben...')
                await message.channel.send('``(ben stop) untuk memberhentikan ben``')

                # TODO: add text limit/allow a stop command while bot is speaking
                # disconnect voice when bot is finished speaking
                while voice_client.is_playing():
                    continue
                await voice_client.disconnect()
                """Post To MongoDB"""
                #post = {"_id": randrange(200), "userid": }
                #Collection.insert_one()
                Ben_InsertData(randrange(200), message.channel.id, message.author.id, guild)

            elif Ben_Exist("guildid", guild) == True:
                dataDB =  Ben_FindGuild(guild)
                memberid = dataDB["memberid"]
                await message.channel.send("Ben sudah dipanggil lebih dulu oleh: <@" + str(memberid) + ">")

        elif 'ben stop' in cmd:
            guild = message.guild
            try:
                dataDB =  Ben_FindGuild(guild.id)
                channel = self.bot.get_channel(dataDB["channelid"])
                if dataDB["memberid"] is not None:
                    if message.author.id == dataDB["memberid"]:
                        await channel.send(f"<:ben:955393615897694228>:\n*Ended call with* <@{message.author.id}>")
                        """Delete Document"""
                        Ben_Delete(dataDB)
                        await message.guild.voice_client.disconnect()
                        return True
            except:
                return False

        try:
            dataDB =  Ben_FindGuild(guild)
            if message.channel.id == dataDB["channelid"]:
                if not message.author.bot:
                    if cmd[0][0] != '>' and cmd != "ben call":
                        res = ['Yes', 'No', 'bleughh', 'Hohoho'] 
                        randomanswer = res
                        
                        """Trying to Disconect"""
                        try:
                            await voice_client.disconnect()
                        except:
                            pass
                        
                        try:
                            channel = message.author.voice.channel
                        except AttributeError:
                            return False
                        
                        """Qualifikasi jawaban"""
                        if listToString(randomanswer) == 'Yes':    
                            """Voice Join"""  
                            voice_client = await channel.connect()                
                            await message.channel.send("<:ben:955393615897694228>:\n" + "Yes")
                            audio_source = await discord.FFmpegOpusAudio.from_probe(source=f'{cwd}/cogs/data/Yes.mp3')
                            voice_client.play(audio_source)
                            # TODO: add text limit/allow a stop command while bot is speaking
                            # disconnect voice when bot is finished speaking
                            while voice_client.is_playing():
                                continue

                            await asyncio.sleep(2)
                            await voice_client.disconnect()
                            return True

                        elif listToString(randomanswer) == 'No':
                            """Voice Join"""  
                            voice_client = await channel.connect()                                
                            await message.channel.send("<:ben:955393615897694228>:\n" + "No")
                            audio_source = await discord.FFmpegOpusAudio.from_probe(source=f'{cwd}/cogs/data/No.mp3')
                            voice_client.play(audio_source)
                            # TODO: add text limit/allow a stop command while bot is speaking
                            # disconnect voice when bot is finished speaking
                            while voice_client.is_playing():
                                continue

                            await asyncio.sleep(2)
                            await voice_client.disconnect()                         
                            return True

                        elif listToString(randomanswer) == 'bleughh':
                            """Voice Join"""  
                            voice_client = await channel.connect()                                
                            await message.channel.send("<:ben:955393615897694228>:\n" + "bleughh")
                            audio_source = await discord.FFmpegOpusAudio.from_probe(source=f'{cwd}/cogs/data/Ugh.mp3')
                            voice_client.play(audio_source)
                            # TODO: add text limit/allow a stop command while bot is speaking
                            # disconnect voice when bot is finished speaking
                            while voice_client.is_playing():
                                continue

                            await asyncio.sleep(2)
                            await voice_client.disconnect()                          
                            return True

                        elif listToString(randomanswer) == 'Hohoho':
                            """Voice Join"""  
                            voice_client = await channel.connect()                                
                            await message.channel.send("<:ben:955393615897694228>:\n" + "Hohoho")
                            audio_source = await discord.FFmpegOpusAudio.from_probe(source=f'{cwd}/cogs/data/Hohoho.mp3')
                            voice_client.play(audio_source)
                            # TODO: add text limit/allow a stop command while bot is speaking
                            # disconnect voice when bot is finished speaking
                            while voice_client.is_playing():
                                continue

                            await asyncio.sleep(2)
                            await voice_client.disconnect()                         
                            return True                    
        except:
            return False

        

def setup(bot):
    bot.add_cog(BenCog(bot))