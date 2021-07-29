#####################################################
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import wikipedia
from saucenao_api import SauceNao
import requests
import json
#####################################################

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['grated'])
    async def img(self, ctx):
      url = f'https://gdvn-static.vnpower.repl.co/lewdpower/G-Rated/{random.randint(1,118)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command()
    async def ecchi(self, ctx):
      url = f'https://gdvn-static.vnpower.repl.co/lewdpower/Ecchi/{random.randint(1,80)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command(aliases=['nsfw', 'hent'])
    async def hentai(self, ctx):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(
                url=
                f'https://gdvn-static.vnpower.repl.co/lewdpower/He/0{random.randint(1,108)}.jpg'
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(
                name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))