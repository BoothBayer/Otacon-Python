import math
import discord
from discord.ext import commands
import logging

#---------Logging--------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#-----------------------
#This is Trouble In Terrorist Town (aka TTT/ttt)
#TTT is a gamemode stemming from counter strike, where you play as terrorist and certain players are selected as traitors
#The traitors must kill the terrorists to win the game
#Detective may exist depending on the quantity of traitors & player preference.
#They are the only ones to be considered truly Innocent since they are identifiable by all players
#There is more to it then this, but who is really reading these comments
#-----------------------

class TTT(commands.Cog):
#add, remove, decide & send, post
#model DICTIONARY: {key=uesrid values={userName, role} , ...}
	def __init__(self,bot):
		self.client = bot

	detectiveCount = 0
	traitorCount = 0
	innocentCount = 0
	traitor_pct = 0.25
	traitor_max = 5
	detective_pct = 0.13
	detective_max = 2
	detective_min_players = 5
	roleCoices = ["Innocent", "Traitor", "Detective"]
	terr = {} #dictionary of persons (i.e. terrorirst)
#	print(f'dic:{terr}')
	@commands.command()
	async def addMe(self, ctx): #There is no check needed to see if the user is already in the list or not, because it would just overwrite their last dictionary entry
		user = ctx.message.author
		self.terr[user.id] = {'name': user.display_name, 'role': 'Innocent'}
		self.terr[user.id + 1] = {'name': "Thing 1", 'role': 'Innocent'} #DELETE
		self.terr[user.id + 2] = {'name': "Thing 2", 'role': 'Innocent'} #DELETE
		self.terr[user.id + 3] = {'name': "Thing 3", 'role': 'Innocent'} #DELETE
		self.terr[user.id + 4] = {'name': "Thing 4", 'role': 'Innocent'} #DELETE
		self.terr[user.id + 5] = {'name': "Thing 5", 'role': 'Innocent'} #DELETE
		for x in self.terr: #DELETE
			print(f'{x} >>> {self.terr[x]}') #DELETE
		await ctx.send(self.terr)
		await ctx.send(f'{user.display_name} has been successfully added!')

	@addMe.error
	async def addMeError(self,ctx,error):
		await ctx.send(f'addMe: An unexpected error has occurred:\n{error}')
		logger.error(error)
		print(f'addMe: An unexpected error has occurred:\n{error}')

	@commands.command()
	async def removeMe(self,ctx):
		user = ctx.message.author
		del self.terr[user.id]
		for x in self.terr: #DELETE
			print(f'{x} >>> {self.terr[x]}') #DELETE
		await ctx.send(f'{user.display_name} has been successfully removed ):')

	@removeMe.error
	async def removeMeError(self,ctx,error):
		await ctx.send(f'removeMe: An unexpected error has occurred:\n{error}')
		logger.error(error)
		print(f'removeMe: An unexpected error has occurred:\n{error}')

	@commands.command()
	async def listPlayers(self,ctx):
		print('listPlayers')
		user = ctx.message.author
		msg = ''
		for id in self.terr: #retrieves all players names
			msg += (f"{self.terr[id]['name']}\n") #adds name to the list
		await ctx.send(f'PLAYERS\n{msg}')

	@listPlayers.error
	async def listPlayersError(self,ctx, error):
		await ctx.send(f'listPlayers: An unexecpted error has occurred:\n{error}')
		logger.error(error)
		print(f'listPlayers: An unexecpted error has occurred:\n{error}')

	@commands.command()
	async def start(self,ctx):
		if len(self.terr) < 4:
			await ctx.send("Not enough player for a game, you require a minimum of 4")
			return
		await ctx.send(f'I am distributing the roles, this may take a minute')
		self.generateRoles(len(self.terr))

	def generateRoles(totalPlayers):
		print("GENERATING ROLES")
		logger.info("GENERATING ROLES")
		#reset data
		self.traitorCount = 0
		self.innocentCount = 0
		self.detectiveCount = 0
		#CALL TRAITOR AND DETECTIVE COUNT
		self.traitorCount = self.getTraitorCount(totalPlayers)
		self.detectiveCount = self.getDetectiveCount(totalPlayers)
		print(f'There will be:\n{self.traitorCount} traitors\n{self.detectiveCount} detectives\n and the rest will be Innocent') #print into chat too?
		x = 0
		player = 0 #in C# it was -1...why? I need to investigate more
		while (x < self.detectiveCount): #x is the amount of detectives currently had
			player++ #iterate one player
			if (player != (len(self.terr)-1)):
				if 

	def getTraitorCount(totalPlayers):
		print("getTraitorCount")
		logger.info("Getting Amount of Traitors")
		traitorTotal = math.floor(totalPlayers * self.traitor_pct)
		if ((traitorTotal >= 1) and (traitorTotal <= self.traitor_max)):
			return traitorTotal
		else:
			return 1

	def getDetectiveCount(totalPlayers):
		print("getDetectiveCount")
		logger.info("Getting amount of Detectives")
		if (totalPlayers >= this.detective_min_players):
			detectiveTotal = math.floor(totalPlayers * self.detective_pct)
			if (detectiveTotal >= 1) and (detectiveTotal <= self.detective_max):
				return detectiveTotal
			else:
				return 0

def setup(bot):
	bot.add_cog(TTT(bot))
