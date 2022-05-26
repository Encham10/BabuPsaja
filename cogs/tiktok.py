from discord.ext import commands
from discord.ext.commands import Cog
from cogs.data.console import *

import os
import re
import aiohttp
import asyncio
import pyppeteer
import discord
import logging
import math

from discord.ext import tasks
from replit import db

db["errors"] = 0
# from keep_alive import keep_alive

# workingDir = os.getcwd()

downloadCount = 0

async def run_command(video_full_path, output_file_name, target_size):
	pro1 = await asyncio.create_subprocess_exec(*["ffprobe", "-v", "error", "-show_entries","format=duration", "-of","default=noprint_wrappers=1:nokey=1", video_full_path], stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
	print("Started: %s, pid=%s" % (pro1, pro1.pid), flush=True)
	stdout, stderr = await pro1.communicate()
	print(float(stdout))
	bitrate = str(math.floor(8*8100/float(stdout))-32)+"k"
	print(bitrate)

	# consider making very fast not ultrafast
	cmd = f"ffmpeg -y -i {video_full_path} -c:v libx264 -passlogfile {video_full_path}passlog -preset ultrafast -b:v {bitrate} -pass 1 -an -f mp4 {output_file_name}"
	print(cmd)

	cmd2 =f"ffmpeg -y -i {video_full_path} -c:v libx264 -passlogfile {video_full_path}passlog -preset ultrafast -b:v {bitrate} -pass 2 -c:a aac -b:a 32k {output_file_name}"
	print(cmd2)

	pro1 = await asyncio.create_subprocess_exec(*cmd.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
	)
	print("Started: %s, pid=%s" % (pro1, pro1.pid), flush=True)
	stdout, stderr = await pro1.communicate()
	
	pro1 = await asyncio.create_subprocess_exec(*cmd2.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
	)
	print("Started: %s, pid=%s" % (pro1, pro1.pid), flush=True)
	stdout, stderr = await pro1.communicate()

	os.remove(video_full_path +"passlog-0.log")
	print(os.path.getsize(output_file_name))
	os.remove(video_full_path)



async def downloadTiktok(url):
	# gets the downloadCount (for the file name) and increments it one
	global downloadCount
	localDow = downloadCount
	downloadCount += 1
	try:
		# print(url)
		print("starting process")
		browser = await pyppeteer.launch({
			'headless': True,
			"args": ['--no-sandbox', '--disable-setuid-sandbox'],
		});
		
		page = await browser.newPage()
		await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36')
		# await page.setDefaultNavigationTimeout(1000000)
		await page.goto(url, {"waitUntil": 'load', "timeout": 1000000})
		try:
			element = await page.querySelector('video')
			videoUrl = await page.evaluate('(element) => element.src', element)
		except:
			try:
				await page.goto(url, {"waitUntil": 'load', "timeout": 1000000})
				await page.waitForSelector('video')
				# await page.waitFor(2000);
				
				# await page.screenshot({'path': 'example.png'})
				# changed from searching for "video"
				element = await page.querySelector('video')
				videoUrl = await page.evaluate('(element) => element.src', element)
			except:
				await page.goto(url, {"waitUntil": 'load', "timeout": 1000000})
				# await page.waitForSelector('video')
				# await page.waitFor(2000);
				
				# await page.screenshot({'path': 'example.png'})
				# changed from searching for "video"
				element = await page.querySelector('video')
				videoUrl = await page.evaluate('(element) => element.src', element)

		# print(videoUrl)
		#gets the video captions
		try:
			cap = await page.querySelector('.tiktok-1ejylhp-DivContainer.e11995xo0')
			capt = await page.evaluate('(element) => element.innerText', cap)
			print(capt)
		except Exception as e: 
			print(e)
			capt = "No Caption"
		#get the likes comments and shares
		try:
			LiCoShData = await page.querySelectorAll('.tiktok-1xiuanb-ButtonActionItem.e1bs7gq20')
			print(LiCoShData)
			LiCoSh = []
			for i in LiCoShData:
				LiCoSh.append(await page.evaluate('(element) => element.innerText', i))
			# print(LiCoSh)
		except Exception as e: 
			db["errors"] += 1
			print(e)
			LiCoSh = ["error","error","error"]
		if(LiCoSh == []):
			LiCoSh = ["error","error","error"]
		print(LiCoSh)
		#get poster image
		try:
			imgobj = await page.querySelector('.tiktok-1zpj2q-ImgAvatar.e1e9er4e1')
			imgsrc = await page.evaluate('(element) => element.src', imgobj)
		except Exception as e: 
			print(e)
			db["errors"] += 1
			imgsrc = ""

		#get poster name
		try:
			posternameObj = await page.querySelector('h3.tiktok-debnpy-H3AuthorTitle.e10yw27c0')
			postername = await page.evaluate('(element) => element.innerText', posternameObj)
		except Exception as e: 
			print(e)
			postername = ""
		# print(postername)

		#get costum file names (might brake?)
		localDow = "".join(x for x in capt[0:15] if x.isalnum()) + str(localDow)

		# print(videoUrl)
		cookies = await page.cookies()
		await browser.close()
	
		chunk_size = 4096

		# custom headers these seem to work almost always
		headers = {
			"Connection": "keep-alive",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
			"Referer": "https://www.tiktok.com/"
		}

		jar = {}
		for selenium_cookie in cookies:
			jar[selenium_cookie['name']] = selenium_cookie['value']

		# downloads the file using the cookies and headers gotten from a browser
		async with aiohttp.ClientSession() as session:
			async with session.get(videoUrl,headers=headers,cookies=jar) as resp:
				if resp.status == 200:
					with open(str(localDow) + ".mp4", 'wb') as fd:
						async for data in resp.content.iter_chunked(chunk_size):
							fd.write(data)

		pathToLastFile = str(localDow) + ".mp4"
		print(os.path.getsize(pathToLastFile));

		#sends the file off to compression if it is over 8 mb
		if(os.path.getsize(pathToLastFile) >= 8388000):
			print("compressing ...")
			await run_command(pathToLastFile, pathToLastFile + "comp.mp4", 8388000)
			pathToLastFile = pathToLastFile + "comp.mp4"
		
		db["dataSent"] += os.path.getsize(pathToLastFile)
		#returns the path to the file
		return(pathToLastFile,capt,LiCoSh,imgsrc,postername)
	except Exception as e: 
		db["errors"] += 1
		print(e)
		# closes the browser if it is open 
		try:
			await browser.close()
		except:
			pass

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def getGuildName(n):
  return [n.name, n.member_count]

def getNum(obj):
	return obj[1]

class TiktokCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #is server dead?
        #is this code breaking everything
        # if(str(message.guild) in db["discordsUsingBot"]):
        # 	# print(db["discordsUsingBot"].index(str(message.guild)))
        # 	db["listOfDiscordsMess"][db["discordsUsingBot"].index(str(message.guild))] += 1
            # print(db["listOfDiscordsMess"][db["discordsUsingBot"].index(str(message.guild))])
            
        # we do not want the bot to reply to itself
        if message.author.id == self.bot.user.id:
            return	

        elif message.content.lower().startswith('&getdata'):
            if(str(message.author.id) == "322193320199716865"):
                print('Logged in as')
                print(self.bot.user.name)
                print(self.bot.user.id)
                guildsSm =list(map(getGuildName, self.bot.guilds))
                
                guildsSm.sort(key=getNum)
                totalusers = 0
                for i in guildsSm:
                    totalusers += i[1]
                print("Data Sent: " + str(db["dataSent"]/8388608*8))
                strTosend = 'Logged in as ' + self.bot.user.name + str(self.bot.user.id) + "\nTotal Users: " + str(totalusers) + "\nTotal Servers: " + str(len(self.bot.guilds)) + "\nTiktoks Converted: " + str(db["tiktoksConverted"])+"\nData Sent: " + str(db["dataSent"]/8388608*8) + "\nTotal discords using bot " + str(len(db["discordsUsingBot"]))+"\nTotal users using bot " + str(len(db["uniqueUsersUsed"]))

                await message.channel.send(strTosend)
                await message.channel.send(guildsSm)
                await message.channel.send("discords using bot: "+ str(db["discordsUsingBot"]))


        # tries to download if it sees .tiktok. in a message
        elif (re.search("\.tiktok\.", message.content) != None):
            if(str(message.guild) in ["nachwile","nachwile2"] or str(message.author.id) == "937842804875460658"):
                print("spammer")
                # try:
                # 	link = await message.channel.create_invite(max_age = 300)
                # 	print(link)
                # except:
                # 	print("blocked linked")
                # await message.channel.send('stop spamming please, join server and talk to me https://discord.gg/ApdPE6adRc', mention_author=True)
                raise Exception("spammer")
            toEdit = await message.channel.send('working on it', mention_author=True)
            if(re.search(" ", message.content) != None):
                print("bad string")
                splitonSpace = message.content.split()
                print(splitonSpace)
                for i in range(len(splitonSpace)):
                    if(re.search("\.tiktok\.", splitonSpace[i]) != None):
                        message.content = splitonSpace[i]

                delOrinoal = False
            else:
                delOrinoal = True
            try:

                print(message.guild)
                fileLoc, capt, LiCoShare, avaSrc, postername = await downloadTiktok(message.content)
                # print(message.guild)
                if(str(message.author.id) not in db["uniqueUsersUsed"]):
                    db["uniqueUsersUsed"].append(str(message.author.id))
                if(str(message.guild) not in db["discordsUsingBot"]):
                    db["discordsUsingBot"].append(str(message.guild))
                    db["listOfDiscordsMess"].append(0)
                else:
                    db["listOfDiscordsMess"][db["discordsUsingBot"].index(str(message.guild))] += 1
                file = discord.File(fileLoc)
                # getting rid of the querry string (not sure if I should try)
                linkToSend = re.findall("([^\?]+)(\?.*)?", message.content)[0][0]
                # print(linkToSend)
                embed=discord.Embed(url=linkToSend, description=message.content, color=discord.Color.blue())


                # uses the authors nick name if they have one
                try:
                    # if(message.author.nick != None):
                    # 	embed.set_footer(text="requested by: "+str(message.author.nick), icon_url=message.author.avatar.url)
                    # else:
                    embed.set_footer(text="requested by: "+str(message.author), icon_url=message.author.avatar.url)
                except:
                    print("pm")
                    embed.set_footer(text="requested by: "+str(message.author), icon_url=message.author.avatar.url)
                LikesComString = ":heart: " + LiCoShare[0] +" :speech_left: " +LiCoShare[1]+ " :arrow_right: " + LiCoShare[2]

                try:
                    # print("caption= "+ capt)
                    if(capt == ""):
                        capt = "no caption"
                    
                    embed.add_field(name=capt, value=LikesComString, inline=True)

                    # embed.set_footer(text=postername, icon_url=avaSrc)
                    embed.set_author(name=postername, icon_url=avaSrc, url="https://www.tiktok.com/@"+str(postername))
                except Exception as e: 
                    db["errors"] += 1
                    print(e)
                toReact = await message.channel.send(embed=embed,file=file)
                await toReact.add_reaction("❌")
                db["tiktoksConverted"] += 1
                print(fileLoc)
                os.remove(fileLoc)
                await toEdit.delete()
                #tries to delete the user sent message 
                if(delOrinoal):
                    try:
                        await message.delete()
                    except:
                        print("no perms")
            except Exception as e: 
                db["errors"] += 1
                print(e)
                try:
                    os.remove(fileLoc)
                    print("failed after download")
                except:
                    print("faild never downloaded")
                try:
                    await toEdit.delete()
                except:
                    print("not able to delete working on it")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            # Make sure that the message the user is reacting to is the one we care about.
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            # print(payload.channel_id)
            user = payload.member
            # print(payload)
            if message.author.id != self.bot.user.id:
                    return
            # print(message.embeds[0].author.url.split("/")[-1])
            # check if the clicker is the orinional sender
            if(str(user).split(" ")[-1] == message.embeds[0].footer.text.split(" ")[-1] and payload.emoji.name =='❌'): 
                await message.delete()
        except Exception as e: 
            print(e)

def setup(bot):
    bot.add_cog(TiktokCog(bot))