import discord
from discord.ext import commands, tasks
import random
import json
import os
import asyncio
from discord.ext.commands.cooldowns import BucketType

async def get_prefix(bot, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        prefixes[str(message.guild.id)] = 'l!'

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        return prefixes[str(message.guild.id)]

async def help2(bot, ctx):
    count = 0
    commands = list(bot.cogs.values())
    
    embed = discord.Embed(colour=discord.Colour.blurple(), title="Help command!", description=f"My current prefix is `{await get_prefix(bot, ctx)}`")
    embed.set_footer(text=f"Type `{await get_prefix(bot, ctx)}help` with a name of a type to see all of the commands! (Currently have {len(bot.commands)})")
    for command in commands:
        if str(command.description) != '':
            embed.add_field(name=f"{command.qualified_name}", value=f"{command.description}", inline=True)
        else:
            embed.add_field(name=f"{command.qualified_name}", value=f"`No description provided`", inline=True)
    await ctx.send(embed=embed)

class Config(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		with open('translation/servers.json', 'r') as f:
			self.servers = json.load(f)

	@commands.command(hidden=True)
	async def load(self, ctx, extension):
		if str(ctx.author) == 'VnPower#8888':
			self.bot.load_extension(f'cogs.{extension}')
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name=f'Loaded {extension} successfully!')
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name='You don\'t have permissions to do that! This is a special command!')
			await ctx.send(embed=embed)

	@commands.command(hidden=True)
	async def unload(self, ctx, extension):
		if str(ctx.author) == 'VnPower#8888':
			self.bot.unload_extension(f'cogs.{extension}')
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name=f'Unloaded {extension} successfully!')
			await ctx.send(embed=embed)
		else:
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name='You don\'t have permissions to do that! This is a special command!')
			await ctx.send(embed=embed)

	@commands.cooldown(1, 10, commands.BucketType.member)
	@commands.command()
	async def change_lang(self, ctx):
		embed = discord.Embed(colour=discord.Colour.blurple())
		f = open('data.json')
		data = json.load(f)
		if str(self.bot.lang) == 'en':
			self.bot.lang = 'vi'
			embed.set_author(name="Changed bot's language to Vietnamese!")
		elif str(self.bot.lang) == 'vi':
			self.bot.lang = 'en'
			embed.set_author(name="Changed bot's language to English!")
		await ctx.send(embed=embed)
		out_file.close()

	@commands.cooldown(1, 60, commands.BucketType.guild)
	@commands.command(description="Reload all cogs", aliases=['rall'])
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
			embed = discord.Embed(title='Reloaded all extensions', color=ctx.me.color, description=to_send, delete_after=10)
			await message.edit(embed=embed)

	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	@commands.command(aliases=['change_prefix'], description="Change server's bot prefix.")
	async def prefix(self, ctx, *, prefixset:str = 'l!'):
		with open('data/prefixes.json', 'r') as f:
			prefixes = json.load(f)

		old_prefix = await get_prefix(self.bot, ctx)
		prefixes[str(ctx.guild.id)] = prefixset

		with open('data/prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		embed = discord.Embed(colour=discord.Colour.blurple(), description=f"Changed server's bot prefix from `{old_prefix}` to `{prefixset}`")
		await ctx.send(embed=embed)

	@commands.command(aliases=['help'], description="Halp!!!!")
	async def h(self, ctx, *, words:str):
	    r1 = self.bot.get_cog(words.capitalize())
	    try:
	        commands = r1.get_commands()
	    except AttributeError:
	        commands = list(self.bot.commands)
	        embed = discord.Embed(colour=discord.Colour.blurple())
	        for i in commands:
	            if str(i.name).lower() == words.lower().strip():
	                embed = discord.Embed(colour=discord.Colour.blurple(), description=i.description)
	                embed.set_author(name=i.name.capitalize())
	                if len(i.aliases) == 0:
	                    embed.add_field(name="Aliases: ", value='None', inline=True)
	                else:
	                    embed.add_field(name="Aliases: ", value=', '.join(str(p) for p in i.aliases), inline=True)
	                embed.add_field(name="Category: ", value=f"`{i.cog_name}`", inline=True)
	                await ctx.send(embed=embed)
	                return
	        embed.title = f"That command or category doesn't exist!"
	        embed.description = f"Try `{get_prefix(bot, ctx)}help` to get category and commands!"
	        await ctx.send(embed=embed)
	        pass
	    else:
	        commands = r1.get_commands()

	        embed = discord.Embed(colour=discord.Colour.blurple(), title=f"{words.capitalize()} commands!")
	        for command in commands:
	            embed.add_field(name=command.name, value=f"`{command.description}`", inline=False)
	        await ctx.send(embed=embed)

	@h.error
	async def error(self, ctx, error):
	    if isinstance(error, commands.MissingRequiredArgument):
	        await help2(self.bot, ctx)


def setup(bot):
	bot.add_cog(Config(bot))