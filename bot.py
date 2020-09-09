import os
import discord
import logging
from discord.ext import commands
import json

#------Logging--------
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#----------------------

#------JSON--------
with open('bot.conf') as json_file:
	data = json.load(json_file)
	ownerID = data['ownerID']
	botToken = data['key']
#------------------

class NoPrivateMessages(commands.CheckFailure):
	pass

def guild_only():
	async def predicate(ctx):
		if ctx.guild is None:
			raise NoPrivateMessages('No Private Messages.')
		return True
	return commands.check(predicate)

def checkName(): #currently set to SoothSayer id
	async def predicate(ctx):
		return ctx.author.id == ownerID
	return commands.check(predicate)

def is_in_guild(guildId):
	async def predicate(ctx):
		return ctx.guild and ctx.guild.id == guildId
	return commands.check(predicate)

#declare command prefix
bot = commands.Bot(command_prefix='$', case_insensitive=True)

@bot.command()
@commands.is_owner()
async def load(ctx,extension):
	print(f'Loading {extension}')
	bot.load_extension(f'cogs.{extension}')
	logger.info(f'Loading {extension}')

@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
	print(f'Unloading {extension}')
	bot.unload_extension(f'cogs.{extension}')
	logger.info(f'Unloading {extension}')

@bot.command()
@commands.is_owner()
async def reload(ctx,extension):
	print(f'Unloading {extension}')
	bot.unload_extension(f'cogs.{extension}')
	print(f'Loading {extension}')
	bot.load_extension(f'cogs.{extension}')
	logger.info(f'Reloaded {extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
@commands.is_owner()
async def quit(ctx):
	print("quitting")
	logger.info("quitting")
	exit()

@quit.error
async def quit_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send('Failed Checks, you do not have the valid credentials')
		logger.info('User attempted to quit bot')

async def on_ready():
	print("Bot is live")

bot.run(botToken)
