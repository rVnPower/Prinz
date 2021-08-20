#####################################################
import discord
from discord.ext import commands, tasks
import json
import requests
#####################################################

class Gd(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Get information of a Geometry Dash level")
	async def gd_level(self, ctx, ID:int):
		r = requests.get(f'https://gdbrowser.com/api/level/{ID}').json()
		if r != '-1':
			embed = discord.Embed(colour=discord.Colour.blurple(), title=r['name'])	
			embed.set_author(name=r['author'])
			embed.add_field(name="Description: ")
			embed.add_field(name="ID: ", value=r['id'])
			embed.add_field(name='Difficulty: ', value=r['difficulty'])
			embed.add_field(name="Length: ", value=r['length'])
			embed.add_field(name="Featured: ", value=r['featured'])
			embed.add_field(name="Downloads:", value=r['downloads'])
			embed.add_field(name="Likes: ", value=r['likes'])
			embed.add_field(name="Required game version: ", value=r['gameVersion'])
			embed.add_field(name="Song: ", value=f"{songID} - {songName}")
		else:
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name="That level does not exist!")
		await ctx.send(embed=embed)

	@commands.command(description="Get information of a Geometry Dash player")
	async def gd_player(self, ctx, *, words):
		r = requests.get(f'https://gdbrowser.com/api/profile/{words}').json()
		embed = discord.Embed(colour=discord.Colour.blurple())
		if r != '-1':
			embed.set_author(name=r['username'])
			embed.add_field(name="Player ID: ", value=r['playerID'])
			if int(r['rank']) == 0:
				embed.add_field(name="Rank: ", value="None")
			else:
				embed.add_field(name="Rank: ", value=r['rank'])
			embed.add_field(name="Stars: ", value=r['stars'])
			embed.add_field(name="Diamonds: ", value=r['diamonds'])
			embed.add_field(name="Secret coins: ", value=r['coins'])
			embed.add_field(name="User coins:", value=r['userCoins'])
			embed.add_field(name="Demons:", value=r['demons'])
			embed.add_field(name="Creator points: ", value=r['cp'])
		if r == '-1':
			embed.set_author(name="That player does not exist!")
		await ctx.send(embed=embed)

	@commands.command(description="Search something in Geometry Dash")
	async def gd_search(self, ctx, *, words):
		r = requests.get(f"https://gdbrowser.com/api/search/{words}?page=1").json()
		embed = discord.Embed(colour=discord.Colour.blurple())
		if r != '-1':
			for i in r:
				embed.set_author(name=f"Search results of {words} in Geometry Dash!")
				embed.add_field(name=f"{i['name']}", value=f"Likes: {i['likes']} | Downloads: {i['downloads']}")
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Gd(bot))