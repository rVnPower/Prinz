#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
#####################################################

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rI'])
    async def randomImg(self, ctx):
        response = requests.get("https://git.meewmeew.info/data/alime.json").json()
        data = requests.get(random.choice(list(response['nsfw'].items()))[1]).json() or requests.get(random.choice(list(response['sfw'].items()))[1]).json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your random image!')
            embed.set_image(url=data['data']['response']['url'])
            embed.set_footer(text="Enjoy.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['grated'])
    async def img(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/G-Rated/{random.randint(1,145)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command()
    async def ecchi(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/Ecchi/{random.randint(1,82)}.jpg'
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
                f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/He/{random.randint(1,108)}.jpg'
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(
                name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['nekoEro', 'nE'])
    async def neko_ero(self, ctx):
        data = requests.get('https://api.nekos.dev/api/v3/images/nsfw/img/neko_ero/').json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            embed.set_footer(text="Type: Neko Lewd. So bad for catgirls... <:terrified:864482152451014667>")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['classicLewd', 'cL'])
    async def classic_lewd(self, ctx):
        data = requests.get('https://api.nekos.dev/api/v3/images/nsfw/img/classic_lewd/').json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            embed.set_footer(text="Type: Classic Lewd. It's classic! <:eyes:>")
            await ctx.send(embed=embed)
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['feetLewd', 'fL'])
    async def feet_lewd(self, ctx):
        data = requests.get('https://api.nekos.dev/api/v3/images/nsfw/img/feet_lewd/').json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            embed.set_footer(text="Type: Feet Lewd. You really love those bare feets, don't you? <:eyes:>")
            await ctx.send(embed=embed)
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))