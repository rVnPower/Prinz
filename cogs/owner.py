import discord
from discord.ext import commands, tasks
import json, typing
import os
import asyncio
import traceback
from discord.ext.commands.cooldowns import BucketType

from config import BOT_PREFIX
from utils.embed import error_embed, normal_embed

import gettext

t = gettext.translation('owner', 'locale', fallback=True)
_ = t.gettext


# async def get_prefix(bot, message):
# 	with open('data/prefixes.json', 'r') as f:
# 		prefixes = json.load(f)

# 	try:
# 		return prefixes[str(message.guild.id)]
# 	except KeyError:
# 		prefixes[str(message.guild.id)] = 'l!'

# 		with open('prefixes.json', 'w') as file:
# 			json.dump(prefixes, file, indent=4)
# 		return prefixes[str(message.guild.id)]

class Config(commands.Cog, description="For admin", name="Config"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	@commands.is_owner()
	async def load(self, ctx, extension):
		self.bot.load_extension(f'cogs.{extension}')
		embed = normal_embed(_(f'Loaded {extension} successfully!'))
		await ctx.send(embed=embed)

	@commands.command(hidden=True)
	@commands.is_owner()
	async def unload(self, ctx, extension):
		self.bot.unload_extension(f'cogs.{extension}')
		embed = normal_embed(f'Unloaded {extension} successfully!')
		await ctx.send(embed=embed)

	@commands.is_owner()
	@commands.command(help="Reload all cogs", aliases=['rall'], hidden=True)
	async def reload_all(self, ctx, argument:str = None):
		cogs_list = ""
		to_send = ""
		err = False
		first_reload_failed_extensions = []
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py"):
				cogs_list = f"{cogs_list} \n🔃 {filename[:-3]}"

		if argument == 'silent' or argument == 's':
			silent = True
		else:
			silent = False
		if argument == 'channel' or argument == 'c':
			channel = True
		else:
			channel = False

		embed = discord.Embed(color=ctx.me.color, description=cogs_list)
		message = await ctx.send(embed=embed)

		for filename in os.listdir("./cogs"):
			if filename.endswith(".py"):
				try:
					self.bot.reload_extension("cogs.{}".format(filename[:-3]))
					to_send = f"{to_send} \n✅ {filename[:-3]}"
				except commands.NoEntryPointError:
					first_reload_failed_extensions.append(filename)

		for filename in first_reload_failed_extensions:
			try:
				self.bot.reload_extension("cogs.{}".format(filename[:-3]))
				to_send = f"{to_send} \n✅ {filename[:-3]}"

			except discord.ext.commands.ExtensionNotLoaded:
				to_send = f"{to_send} \n❌ {filename[:-3]} - Not loaded"
			except discord.ext.commands.ExtensionNotFound:
				to_send = f"{to_send} \n❌ {filename[:-3]} - Not found"
			except discord.ext.commands.NoEntryPointError:
				to_send = f"{to_send} \n❌ {filename[:-3]} - No setup func"
			except discord.ext.commands.ExtensionFailed as e:
				traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
				to_send = f"{to_send} \n❌ {filename[:-3]} - Execution error"
				embed_error = discord.Embed(color=ctx.me.color,
											description=f"\n❌ {filename[:-3]} Execution error - Traceback"
														f"\n```\n{traceback_string}\n```")
				err = True
				await ctx.author.send(embed=embed_error)
		await asyncio.sleep(0.4)
		if err:
			if not silent:
				if not channel:
					to_send = f"{to_send} \n\n📬 {ctx.author.mention}, I sent you all the tracebacks."
				else:
					to_send = f"{to_send} \n\n📬 Sent all tracebacks here."
			if silent:
				to_send = f"{to_send} \n\n📭 silent, no tracebacks sent."
			embed = discord.Embed(color=ctx.me.color, description=to_send, title='Reloaded some extensions')
			await message.edit(embed=embed)
		else:
			embed = discord.Embed(title='Reloaded all extensions', color=ctx.me.color, description=to_send)
			self.bot.owner = ctx.author
			await message.edit(embed=embed)

	@commands.command(aliases = ['setstatus', 'ss', 'activity'])
	@commands.is_owner()
	async def status(self, ctx, type: typing.Optional[str],* , argument: typing.Optional[str]):
		if ctx.author.guild_permissions.administrator == True:
			botprefix = BOT_PREFIX

			if type == None:
				embed = discord.Embed(title= "`ERROR` NO STATUS GIVEN!", description="Here is a list of available types:", color = ctx.me.color)
				embed.add_field(name=(botprefix + 'status Playing <status>'), value='Sets the status to Playing.', inline=False)
				embed.add_field(name=(botprefix + 'status Listening <status>'), value='Sets the status to Listening.', inline=False)
				embed.add_field(name=(botprefix + 'status Watching <status>'), value='Sets the status to Watching.', inline=False)
				await ctx.send(embed=embed, delete_after=45)
				await asyncio.sleep(45)
				await ctx.message.delete()
			else:
				type = type.lower()
			if type == "playing":
				if argument !=  None:
					# Setting `Playing ` status
					await self.bot.change_presence(activity=discord.Game(name=f'{argument}'))
					await ctx.message.add_reaction('✅')
					await ctx.send(f"Activity changed to `Playing {argument}` ", delete_after=10)
					await asyncio.sleep(10)
					await ctx.message.delete()

			if type == "listening":
				if argument != None:
					# Setting `Listening ` status
					await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{argument}'))
					await ctx.message.add_reaction('✅')
					await ctx.send(f"Activity changed to `Listening to {argument}` ", delete_after=10)
					await asyncio.sleep(10)
					await ctx.message.delete()

			if type == "watching":
				if argument !=  None:
					#Setting `Watching ` status
					await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{argument}'))
					await ctx.message.add_reaction('✅')
					await ctx.send(f"Activity changed to `Watching {argument}` ", delete_after=10)
					await asyncio.sleep(10)
					await ctx.message.delete()

			if type == "competing":
				if argument !=  None:
					#Setting `other ` status
					await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f'{argument}'))
					await ctx.message.add_reaction('✅')
					await ctx.send(f"Activity changed to `Competing in {argument}` ", delete_after=10)
					await asyncio.sleep(10)
					await ctx.message.delete()

			if type == "clear":
				await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name='cleared'))
				await ctx.message.add_reaction('✅')
				await ctx.send(f"Activity cleared ", delete_after=10)
				await asyncio.sleep(10)
				await ctx.message.delete()

			if type != "watching" and type != "listening" and type != "playing" and type != "competing" and type != "clear" and type != "4afc07a4055edc68da62f18f7ecdd103":
				embed = discord.Embed(title= "`ERROR` INVALID TYPE!", description="Here is a list of available types:", color = ctx.me.color)
				embed.add_field(name=(botprefix + 'status Playing <status>'), value='Sets the status to Playing.', inline=False)
				embed.add_field(name=(botprefix + 'status Listening <status>'), value='Sets the status to `Listening to`.', inline=False)
				embed.add_field(name=(botprefix + 'status Watching <status>'), value='Sets the status to `Watching`.', inline=False)
				embed.add_field(name=(botprefix + 'status Competing <status>'), value='Sets the status to `Competing in`.', inline=False)
				await ctx.send(embed=embed, delete_after=45)
				await asyncio.sleep(45)
				await ctx.message.delete()
		else:
			await ctx.message.add_reaction('🚫')
			await asyncio.sleep(5)
			await ctx.message.delete()

	@commands.command(aliases=['rel', 're', 'rc'])
	@commands.is_owner()
	async def reload(self, ctx, extension = ""):
		embed = normal_embed(f"🔃 {extension}")
		message = await ctx.send(embed=embed)
		try:
			self.bot.reload_extension("cogs.{}".format(extension))
			await asyncio.sleep(0.5)
			embed = error_embed(f"✅ {extension}")
			await message.edit(embed=embed)
		except discord.ext.commands.ExtensionNotLoaded:
			await asyncio.sleep(0.5)
			embed = error_embed(f"❌ Extension not loaded")
			await message.edit(embed=embed)

		except discord.ext.commands.ExtensionNotFound:
			await asyncio.sleep(0.5)
			embed = discord.Embed(color=ctx.me.color, description = f"❌ Extension not found")
			await message.edit(embed=embed)

		except discord.ext.commands.NoEntryPointError:
			await asyncio.sleep(0.5)
			embed = error_embed(f"❌ No setup function")
			await message.edit(embed=embed)

		except discord.ext.commands.ExtensionFailed as e:
			traceback_string = "".join(traceback.format_exception(etype=None, value=e, tb=e.__traceback__))
			await asyncio.sleep(0.5)
			embed = discord.Embed(color=ctx.me.color, description = f"❌ Execution error\n```{traceback_string}```")
			try: await message.edit(embed=embed)
			except:
				embed = discord.Embed(color=ctx.me.color, description = f"❌ Execution error ```\n error too long, check the console\n```")
				await message.edit()
			raise e
	

def setup(bot):
	bot.add_cog(Config(bot))