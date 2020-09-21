import math
import discord
from discord.ext import commands
import logging
import random

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
#model DICTIONARY: {key=uesrid values={userName, role} , ...}
	def __init__(self,bot):
		self.client = bot

	detectiveCount = 0
	traitorCount = 0
	innocentCount = 0
	traitor_pct = 0.25 #percentage of players that are traitors, and the chance of becoming one. Maybe I should make separate variables for this? who cares though
	traitor_max = 5 #maximum amount of traitors in a game, maybe I should remove this or make it arbitrarily large, not enough feedback to know.
	detective_pct = 0.13
	detective_max = 2
	detective_min_players = 5 #minimum amount of players for a detective to be put into the game
	roleCoices = ["Innocent", "Traitor", "Detective"]
	terr = {} #dictionary of persons (i.e. terrorirst)

	@commands.command()
	async def addVC(self, ctx):
		logger.info("Running addVC")
		users = ctx.message.author.voice.channel.members
		for user in users:
			self.terr[user.id] = {'name': user.display_name, 'role': 'Innocent'}
	@commands.command()
	async def addMe(self, ctx): #There is no check needed to see if the user is already in the list or not, because it would just overwrite their last dictionary entry
		user = ctx.message.author
		self.terr[user.id] = {'name': user.display_name, 'role': 'Innocent'}
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
	async def results(self,ctx):
		for x in self.terr: #DELETE
			print(f'{x} >>> {self.terr[x]}') #DELETE

	@commands.command()
	async def start(self,ctx):
		if len(self.terr) < 4:
			await ctx.send("Not enough player for a game, you require a minimum of 4")
			return
		await ctx.send(f'I am distributing the roles, this may take a minute')
		self.generateRoles(len(self.terr))

	@start.error
	async def startError(self, ctx, error):
		await ctx.send(f'start: An unexpected error has occurred:\n{error}')
		logger.error(error)
		printf(f'start: An unexpected error has ocurred:\n{error}')
	def generateRoles(self, totalPlayers):
		print("GENERATING ROLES")
		logger.info("GENERATING ROLES")
		#reset data
		self.traitorCount = 0 #global variable that must be reset
		self.innocentCount = 0 #global variable that must be reset
		self.detectiveCount = 0 #gloabl variable that must be reset
		detectives = 0 #used in while loop below
		traitors = 0 #used in while loop below
		#CALL TRAITOR AND DETECTIVE COUNT
		self.traitorCount = self.getTraitorCount(totalPlayers)
		self.detectiveCount = self.getDetectiveCount(totalPlayers)
		print(f'There will be:\n{self.traitorCount} traitors\n{self.detectiveCount} detectives\n and the rest will be Innocent') #print into chat too?

		while (detectives < self.detectiveCount):
			for player in self.terr:
				user = self.terr[player]
				if (detectives >= self.detectiveCount):
					break
				ranNum = random.random()
				if (ranNum <= self.detective_pct):
					detectives += 1 #iterate one detective
					user['role'] = 'Detective' #set the role

		while (traitors < self.traitorCount): #keep iterating until we have no more traitors to assign; this is needed because the for loop will not repeat itself
			for player in self.terr: #go through all players once
				user = self.terr[player] #this is quick access variable for the dictionary, just for my ease
				if (traitors >= self.traitorCount): #if we have reached and or exeeded the max amount of traitors, break
					break
				if (user['role'] == 'Innocent'): #Check if they do not have a role assigned to them already(e.g. "Detective")
					ranNum = random.random() #generates a random number to decide if you are the traitor or not
					if (ranNum <= self.traitor_pct): #check if they meet the requirements for lady fate
						traitors += 1 #iterate one traitor
						user['role'] = 'Traitor' #set the role

	def getTraitorCount(self, totalPlayers):
		print("\ngetTraitorCount\n")
		logger.info("Getting Amount of Traitors")
		traitorTotal = math.floor(totalPlayers * self.traitor_pct)
		if ((traitorTotal >= 1) and (traitorTotal <= self.traitor_max)):
			return traitorTotal
		else:
			return 1

	def getDetectiveCount(self, totalPlayers):
		print("\ngetDetectiveCount\n")
		logger.info("Getting amount of Detectives")
		if (totalPlayers >= self.detective_min_players):
			detectiveTotal = math.floor(totalPlayers * self.detective_pct)
			if (detectiveTotal >= 1) and (detectiveTotal <= self.detective_max):
				return detectiveTotal
			else:
				return 0

	async def distributeRoles(self, players):
		logger.info("Distributing Roles")
		for player in players: #loop through all players
			try:
				user = players[player] #ease of access variable
				member = await commands.MemberConverter().convert(ctx, str(player)) #Okay, so this is a doozie. This sets the variable member by converting the discord id into a string and then converting it in the member class. This is all just so we can send a dm.
				dm = await member.create_dm() #open a dm
				await dm.send(f"Hey {user['name']}, your role is {user['role']}") #send message with information into dm
			except:
				logger.error(f"Something went wrong while distributing roles, {players[player]['name']} did not receiver their message.")

def setup(bot):
	bot.add_cog(TTT(bot))
