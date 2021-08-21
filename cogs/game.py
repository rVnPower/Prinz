#####################################################
import discord
from discord.ext import commands, tasks
import random
import asyncio
#####################################################

class Games(commands.Cog, description="Game commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Play a guessing game (Guess a number from 1 to 1000)")
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

def setup(bot):
    bot.add_cog(Games(bot))