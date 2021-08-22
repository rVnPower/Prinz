import discord
from discord.ext import commands, tasks
import random
import json

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
		if str(self.bot.lang) == 'en':
			self.bot.lang = 'vi'
			embed.set_author(name="Changed bot's language to Vietnamese!")
		elif str(self.bot.lang) == 'vi':
			self.bot.lang = 'en'
			embed.set_author(name="Changed bot's language to English!")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Config(bot))