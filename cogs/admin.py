import discord
import logging
from discord.ext import commands
#---------Logging--------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#-----------------------

class Admin(commands.Cog):

	def __init__(self,bot):
		self.client = bot

	@commands.command()
	@commands.is_owner()
	async def say(self,ctx,*,args):
		await ctx.send(args)
	@say.error
	async def sayError(self,ctx,error):
		logger.error(error)
		await ctx.send("An unexpected error has occured")

def setup(bot):
	bot.add_cog(Admin(bot))
