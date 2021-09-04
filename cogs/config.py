import discord
from discord.ext import commands, tasks
import random
import json
import os
import asyncio
import datetime
import contextlib
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

class Config(commands.Cog, description="Bot's configuration commands", name="Config"):
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
	@commands.command(help="Reload all cogs", aliases=['rall'])
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
	@commands.command(aliases=['change_prefix'], help="Change server's bot prefix.")
	async def prefix(self, ctx, *, prefixset:str = 'l!'):
		with open('data/prefixes.json', 'r') as f:
			prefixes = json.load(f)

		old_prefix = await get_prefix(self.bot, ctx)
		prefixes[str(ctx.guild.id)] = prefixset

		with open('data/prefixes.json', 'w') as f:
			json.dump(prefixes, f, indent=4)
		embed = discord.Embed(colour=discord.Colour.blurple(), description=f"Changed server's bot prefix from `{old_prefix}` to `{prefixset}`")
		await ctx.send(embed=embed)
	'''

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
	'''


def setup(bot):
	class HelpEmbed(discord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
	    def __init__(self, **kwargs):
	        super().__init__(**kwargs)
	        self.timestamp = datetime.datetime.utcnow()
	        text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
	        self.set_footer(text=text)
	        self.color = discord.Color.blurple()


	class MyHelp(commands.HelpCommand):
	    def __init__(self):
	        super().__init__( # create our class with some aliases and cooldown
	            command_attrs={
	                "help": "The help command for the bot",
	                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.user),
	                "aliases": ['commands']
	            }
	        )
	    
	    async def send(self, **kwargs):
	        """a short cut to sending to get_destination"""
	        await self.get_destination().send(**kwargs)

	    async def send_bot_help(self, mapping):
	        """triggers when a `<prefix>help` is called"""
	        ctx = self.context
	        embed = HelpEmbed(title=f"Help")
	        embed.set_thumbnail(url=ctx.me.avatar_url)
	        usable = 0 

	        for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
	            if filtered_commands := await self.filter_commands(commands): 
	                # if no commands are usable in this category, we don't want to display it
	                amount_commands = len(filtered_commands)
	                usable += amount_commands
	                if cog: # getting attributes dependent on if a cog exists or not
	                    name = cog.qualified_name
	                    description = cog.description or "No description"
	                else:
	                    name = "No Category"
	                    description = "Commands with no category"

	                embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

	        embed.description = f"{len(bot.commands)} commands | {usable} usable" 

	        await self.send(embed=embed)

	    async def send_command_help(self, command):
	        """triggers when a `<prefix>help <command>` is called"""
	        signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
	        embed = HelpEmbed(title=signature, description=command.help or "No help found...")

	        if cog := command.cog:
	            embed.add_field(name="Category", value=cog.qualified_name)

	        can_run = "No"
	        # command.can_run to test if the cog is usable
	        with contextlib.suppress(commands.CommandError):
	            if await command.can_run(self.context):
	                can_run = "Yes"
	            
	        embed.add_field(name="Usable", value=can_run)

	        if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
	            embed.add_field(
	                name="Cooldown",
	                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
	            )

	        await self.send(embed=embed)

	    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
	        embed = HelpEmbed(title=title, description=description or "No help found...")

	        if filtered_commands := await self.filter_commands(commands):
	            for command in filtered_commands:
	                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
	           
	        await self.send(embed=embed)

	    async def send_group_help(self, group):
	        """triggers when a `<prefix>help <group>` is called"""
	        title = self.get_command_signature(group)
	        await self.send_help_embed(title, group.help, group.commands)

	    async def send_cog_help(self, cog):
	        """triggers when a `<prefix>help <cog>` is called"""
	        title = cog.qualified_name or "No"
	        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

	    async def send_error_message(self, error):
	        embed = discord.Embed(title="Error", description=error)
	        channel = self.get_destination()
	        await channel.send(embed=embed)
	bot.help_command = MyHelp()
	bot.add_cog(Config(bot))