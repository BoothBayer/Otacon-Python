import asyncio
import discord
import logging
from discord.ext import commands
import os
import json
#---------Logging--------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s)'))
logger.addHandler(handler)
#-----------------------

#------JSON--------
with open('bot.conf') as json_file:
	data = json.load(json_file)
	musicDir = data['musicDIR']
#------------------

class Music(commands.Cog):
	def __init__(self,bot):
		self.client = bot

	@commands.command()
	@commands.is_owner()
	async def join(self,ctx):
		channel = ctx.message.author.voice.channel
		await channel.connect()
		logger.info(f'Joining voice channel: {channel}')

	@join.error
	async def joinError(self,ctx,error):
		await ctx.send('An unexpected error has occured')
		logger.error(error)

	@commands.command()
	@commands.is_owner()
	async def leave(self,ctx):
		server = ctx.message.guild
		channel = server.voice_client
		await channel.disconnect()
		logger.info(f'Leaving voice channel: channel')

	@leave.error
	async def leaveError(self,ctx,error):
		await ctx.send('An unexpected error has occured: {error}')
		logger.error(error)

	@commands.command()
	async def play(self, ctx, *,song): #ADD A CHECK THAT UNPAUSES IF A SONG IS PLAYING AND THEN ADD SONG TO QUEUE
		voice_client = ctx.message.guild.voice_client
		if voice_client.is_playing():
			#ADD TO QUEUE
			pass
		elif voice_client.is_paused():
			await voice_client.resume()
		else:
			try:
				audioFile = self.iterDict(self.jukeDirec, song)
			except KeyError:
				print("Name error")
			print(f'Found: {audioFile}')
			try:
				audio = discord.FFmpegPCMAudio(f'{audioFile}', options='-vn') #song
				await voice_client.play(audio)
			except:
				print(f'idk why this happens, but the song is playing now')
			logger.info(f'Playing song: {song} in voice channel: {voice_client.channel}')

	def iterDict(self, dic, search):
		x = None
		for k, v in dic.items():
			if isinstance(v, dict):
				x = self.iterDict(v, search)
				if x != None:
					return x
					break
			elif (v == search):
				x = dic['location']
				print(x)
				break
		return x

	@play.error
	async def playError(self,ctx,error):
		await ctx.send(f'An unexpected error has occured: {error}')
		logger.error(error)
		print(f'An error has occured with the play command:\n{error}')

	@commands.command()
	async def stop(self,ctx):
		voice_client = ctx.message.guild.voice_client
		await voice_client.stop()

	@stop.error
	async def stopError(self,ctx,error):
		await ctx.send(f'An unexpected error has occured: {error}')
		logger.error(error)

	@commands.command()
	async def pause(self,ctx):
		voice_client = ctx.message.guild.voice_client
		await voice_client.pause()

	@pause.error
	async def pauseError(self,ctx,error):
		await ctx.send(f'An unexpected error has occured: {error}')
		logger.error(error)

	@commands.command(aliases=['unpause'])
	async def resume(self,ctx):
		voice_client = ctx.message.guild.voice_client
		await voice_client.resume()

	@resume.error
	async def resumeError(self,ctx,error):
		await ctx.send(f'An unexpected error has occured: {error}')
		logger.error(error)
		print(f'An error has occured with the resume commmand:\n{error}')

	#------indexing music-------- #Do nested disctionaries where a number starting from 1 is the key and the data is another dictionary contaiing name, album=T/F, song = T/F or something of the sort
	jukeDirec = {}
        for root, dirs, files in os.walk(musicDir): #'/home/sooth/Music/'):
		count = 0
		tempDic = {}
		for item in files:
			count = count + 1
			if not (item.endswith('.jpg') or item.endswith('.png')):
				name = item.replace(".mp3","").replace(".flaac", "")
				location = os.path.join(root,item)
				lastCharacter = root.rfind("/")
				album = root[(lastCharacter+1):].lower()
				tempDic[name] = {"location": location, "name": name, "album": album}
				if count == len(files):
					jukeDirec[album] = tempDic

	@commands.command()
	async def showAlbum(self,ctx,*,inputAlbum = ""):
		#create needed variables
		page = [] #contains pages to paginate through
		count = 0 #Counter default start point
		inputAlbum = inputAlbum.lower() #Bring it to lowercase, as our dictionary is set up
		pageBuilder = ""
		#------------Sort-Some-Stuff---------------------
		if (inputAlbum == ""):
			for album in self.jukeDirec:
				if count == 0: #If this is a new loop, add the page number to the top
					embName = (f'Page: {len(page)+1}\n')

				count += 1 #Count one+
				pageBuilder += (f'{album}\n') #Add the album name and create a new line

				if count >= 15: #If we are at, or exceed the max number of iterations add item to list and start a new page
					emb = discord.Embed()
					page.append(emb.add_field(name=embName, value=pageBuilder)) #pageBuilder)
					pageBuilder = ""
					count = 0
		else:
			totalSongs = len(self.jukeDirec[inputAlbum])
			songs = 0
			for song in self.jukeDirec[inputAlbum]:
				songs += 1
				if count == 0: #add page number on new loop
					embName = (f'Page: {len(page)+1}\n')
				count += 1

				name = self.jukeDirec[inputAlbum][song]['name']
				pageBuilder += f'{name}\n' #Add name of song to the message

				if ((count >= 15) or (songs >= totalSongs)): #if we have reached the maximum amount of songs for the page, or the total number of songs create a new page
					emb = discord.Embed()
					page.append(emb.add_field(name=embName, value=pageBuilder)) #Add the mebed to the page list
					pageBuilder = ""
					count = 0

		#--------------pagination-begins--------------------
		currentPage = 0 #What page the message is currently on
		maxPage = len(page) - 1 #The maximum amount of pages
		msg = await ctx.send(embed=page[0]) #send the first page
		reactions = ['⏪','◀️','⏹️','▶️','⏩'] #What reactions should be addded to the message
		for emoji in reactions: #add the reactions
			await msg.add_reaction(emoji)

		def check(reaction, user): #Check for if the user who is reacting is the person who called the command in the first place and if it is the same message
			return ((user == ctx.message.author) and (str(reaction.emoji) in reactions) and (reaction.message.id == msg.id))
		looping = True #Default state of loop
		while looping: #Loop until we call for an end
			done, pending = await asyncio.wait([ #honestly I have no clue how the done and pending work, but I guess it puts the finished tasks in the first variable(done), and the unfinished tasks in the second variable(pending)
						self.client.wait_for('reaction_add', timeout=60.0, check=check),
						self.client.wait_for('reaction_remove', timeout=60.0, check=check)
					], return_when=asyncio.FIRST_COMPLETED) #Whichever event returns first we will take the results from

			try:
				test = done.pop().result() #Delete the results after returning them
				reaction = test[0] #user == test[1] (prints out SoothSayer#0454) #Set the reaction variable so we can get data from it
			except futures.TimeoutError: #if timer runs out, then it ends the script
				looping = False
				await msg.add_reaction('🛑') #indicator so that the user knows the script is done
			else:
				if (str(reaction) == '⏪'): #back to beginning
					currentPage = 0
					await msg.edit(embed=(page[currentPage]))

				elif (str(reaction) == '◀️'): #Go back a page if this is true
					backPage = currentPage - 1
					if backPage >= 0:
						currentPage = backPage
						await msg.edit(embed=(page[backPage]))

				elif (str(reaction) == '▶️'): #go forward a page
					forwardPage = currentPage + 1
					if forwardPage <= maxPage:
						currentPage = forwardPage
						await msg.edit(embed=(page[forwardPage]))
				elif (str(reaction) == '⏩'): #go to end
					currentPage = maxPage
					await msg.edit(embed=(page[forwardPage]))

				elif (str(reaction) =='⏹️'): #stop pagination
					await msg.add_reaction('🛑') #indicator so that the user knows the script is done
					looping = False

			for future in pending: #Stops all coroutines that are not in use
				future.cancel()

	@showAlbum.error
	async def showAlbumError(self,ctx,error):
		await ctx.send(f'An unexpected error has occured:\n{error}')
		logger.error(error)
		print(f'An error has occurred with the show Album command:\n{error}')

def setup(bot):
	bot.add_cog(Music(bot))
