#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
from chessdotcom import get_leaderboards,get_player_stats
#####################################################

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = get_leaderboards().json

    @commands.command(description="Get a category leaderboard on Chess.com")
    async def chess_top(self, ctx, *, words:str = "daily"):
        data2 = self.data['leaderboards']
        categories = self.data['leaderboards'].keys()
        for category in categories:
            if category == words.lower().strip():
                embed = discord.Embed(colour=discord.Colour.blurple(), title=f"Category: {category}")
                embed.set_author(name="Chess.com leaderboard!")
                for player in data2[category]:
                    embed.add_field(name=f"Rank: {player['rank']}", value=f"Username: {player['username']} | Rating: {player['score']}")
                await ctx.send(embed=embed)

    @commands.command(description="Print all of the chess type on Chess.com")
    async def chess_type(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Type of chess on Chess.com")
        embed.add_field(name='- ', value="daily, daily960, live_rapid, live_blitz, live_bullet, live_bughouse, live_blitz960, live_threecheck, live_crazyhouse, live_kingofthehill, tactics")
        await ctx.send(embed=embed)

    @commands.command()
    async def chess_player(self, ctx, *, words:str = "VnPower"):
        def print_leaderboard(self, username):
            data = get_player_stats(username).json()
            categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
            embed = discord.Embed(colour=discord.Colour.blurple(), title=f"{words}'s stats on Chess.com")
            for category in categories:
                embed.add_field(name= f'Category: {category} |', value=f"Current: {data[category]['last']['rating']} | Best: {data[category]['best']['rating']}")
            return embed
        embed = print_leaderboard(words)
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Chess(bot))