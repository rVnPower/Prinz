#####################################################
import discord
from discord.ext import commands, tasks
import json
import requests
import aiohttp
#####################################################

class Gd(commands.Cog, description="Geometry Dash commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Get information of a Geometry Dash level")
	async def gd_level(self, ctx, ID:int):
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://gdbrowser.com/api/level/{ID}') as resp:
				r = await resp.json()
		if r != '-1':
			embed = discord.Embed(colour=discord.Colour.blurple(), title=r['name'])	
			embed.set_author(name=r['author'], inline=True)
			embed.add_field(name="Description: ", inline=True)
			embed.add_field(name="ID: ", value=r['id'], inline=True)
			embed.add_field(name='Difficulty: ', value=r['difficulty'], inline=True)
			embed.add_field(name="Length: ", value=r['length'], inline=True)
			embed.add_field(name="Featured: ", value=r['featured'], inline=True)
			embed.add_field(name="Downloads:", value=r['downloads'], inline=True)
			embed.add_field(name="Likes: ", value=r['likes'], inline=True)
			embed.add_field(name="Required game version: ", value=r['gameVersion'], inline=True)
			embed.add_field(name="Song: ", value=f"{songID} - {songName}")
		else:
			embed = discord.Embed(colour=discord.Colour.blurple())
			embed.set_author(name="That level does not exist!")
		await ctx.send(embed=embed)

	@commands.command(description="Get information of a Geometry Dash player")
	async def gd_player(self, ctx, *, words):
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://gdbrowser.com/api/profile/{words}') as resp:
				r = await resp.json()
		embed = discord.Embed(colour=discord.Colour.blurple())
		if r != '-1':
			embed.set_author(name=r['username'])
			embed.add_field(name="Player ID: ", value=r['playerID'], inline=True)
			if int(r['rank']) == 0:
				embed.add_field(name="Rank: ", value="None", inline=True)
			else:
				embed.add_field(name="Rank: ", value=r['rank'], inline=True)
			embed.add_field(name="Stars: ", value=r['stars'], inline=True)
			embed.add_field(name="Diamonds: ", value=r['diamonds'], inline=True)
			embed.add_field(name="Secret coins: ", value=r['coins'], inline=True)
			embed.add_field(name="User coins:", value=r['userCoins'], inline=True)
			embed.add_field(name="Demons:", value=r['demons'], inline=True)
			embed.add_field(name="Creator points: ", value=r['cp'], inline=True)
		if r == '-1':
			embed.set_author(name="That player does not exist!")
		await ctx.send(embed=embed)

	@commands.command(description="Search something in Geometry Dash")
	async def gd_search(self, ctx, *, words):
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://gdbrowser.com/api/search/{words}?page=1') as resp:
				r = await resp.json()
		embed = discord.Embed(colour=discord.Colour.blurple())
		if r != '-1':
			for i in r:
				embed.set_author(name=f"Search results of {words} in Geometry Dash!")
				embed.add_field(name=f"{i['name']}", value=f"Likes: {i['likes']} | Downloads: {i['downloads']}")
			await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Gd(bot))