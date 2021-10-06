#####################################################
import discord
from discord.ext import commands, tasks
import random
import asyncio
import time
from others.songs import easy
from games import twenty, tictactoe, minesweeper, wumpus
from discord.ext.commands.cooldowns import BucketType
#####################################################

class Games(commands.Cog, description="Games you can play", name="Game"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(help="Play Wumpus")
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def _wumpus(self, ctx):
		await wumpus.play(self.bot, ctx)

	@commands.command(help="Play a guessing game (Guess a number from 1 to 1000)")
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def guess(self, ctx):
		# Simple guessing game
		embed = discord.Embed(colour=discord.Colour.blurple(), title="Guess a number between 1 and 1000.")
		await ctx.send(embed=embed)
		answer = random.randint(1, 1000)
		while True:
			def is_correct(m):
				return m.author == ctx.author and m.content.isdigit()
			embed = discord.Embed(colour=discord.Colour.blurple())

			try:
				guess = await self.bot.wait_for('message', check=is_correct, timeout=60.0)
			except asyncio.TimeoutError:
				embed.set_author(name=f'Sorry, you took too long it was {answer}.')
				await ctx.send(embed=embed)
				break

			if int(guess.content) == answer:
				embed.set_author(name = 'You are right!')
				await ctx.send(embed=embed)
				break
			if int(guess.content) > answer:
				embed.set_author(name='Lower!')
			if int(guess.content) < answer:
				embed.set_author(name ='Higher!')
			await ctx.send(embed=embed)

	@commands.cooldown(1, 30, commands.BucketType.user)
	@commands.command(name='2048', help="Play 2048 game.")
	async def twenty(self, ctx):
		await twenty.play(ctx, self.bot)

	@commands.cooldown(1, 10, commands.BucketType.user)
	@commands.command(aliases=['ttt', 'tic-tac-toe'], help="Play Tic-Tac-Toe")
	async def tictactoe(self, ctx):
		await tictactoe.play_game(self.bot, ctx, chance_for_error=0.2)

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command(name='minesweeper', help="Play Minesweeper")
	async def minesweeper(self, ctx, columns=None, rows=None, bombs=None):
		await minesweeper.play(ctx, columns, rows, bombs)

	@commands.command()
	async def song(self, ctx):
		t1 = time.time()

		async def check():
			return time.time()

		song = random.choice(easy)
		embed = discord.Embed(color=discord.Colour.blurple(), title=f"What is this song? ({song['difficulty']})", description=song['lyric'])
		
		if song['difficulty'] == "Easy":
			embed.color = discord.Colour.green()
		elif song['difficulty'] == "Medium":
			pass
		elif song['difficulty'] == "Hard":
			embed.color = discord.Colour.red()

		await ctx.send(embed=embed)

		while True:
			t2 = await check()
			if t2 - t1 > 15.0:
				embed = discord.Embed(color=discord.Colour.blurple(), title='Times up!')
				await ctx.send(embed=embed)
				return
			else:
				pass

			try:
				guess = await self.bot.wait_for('message')
			except asyncio.TimeoutError:
				embed = discord.Embed(color=discord.Colour.blurple(), title='Times up!')
				await ctx.send(embed=embed)
				return
			if guess.content.lower().strip() == song['name'].lower():
				embed = discord.Embed(color=discord.Colour.blurple(), title=f"It\'s {song['name'].capitalize()}!", description=f"You guessed it correctly, {guess.author.mention}!")
				await ctx.send(embed=embed)
				break
			else:
				pass

	



def setup(bot):
	bot.add_cog(Games(bot))