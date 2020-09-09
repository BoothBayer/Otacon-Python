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

class Basics(commands.Cog):

	def __init__(self,bot):
		self.client = bot

	#gets information about the mentioned user
	@commands.command()
	async def investigate(self, ctx, *, member: discord.Member):
		await ctx.send('NAME {0}\nJOINED AT {0.joined_at}\nGUILD: {0.guild}\nVOICE: {0.voice}'.format(member))

	@investigate.error
	async def investigate_error(self,ctx,error):
		if isinstance(error, commands.BadArgument):
			await ctx.send('I could not find that member')
			logger.error(error)
			print(error)
		if isinstance(error, commands.CheckFailure):
			await ctx.send("You aren't in the right guild buddy")


def setup(bot):
	bot.add_cog(Basics(bot))
