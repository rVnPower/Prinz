#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
from discord_slash import cog_ext, SlashContext
guild_ids = [865509913417482240, 745561266805800990]
#####################################################

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="randomImg", description="Send a random image", guild_ids=guild_ids)
    async def _randomImg(self, ctx):
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

    @cog_ext.cog_slash(name="img", description="Send a random anime image from VnPower's GDrive", guild_ids=guild_ids)
    async def _img(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/G-Rated/{random.randint(1,145)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ecchi", description="Send a random ecchi image", guild_ids=guild_ids)
    async def _ecchi(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/Ecchi/{random.randint(1,82)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="hentai", description="Send a random hentai image", guild_ids=guild_ids)
    async def _hentai(self, ctx):
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

    @cog_ext.cog_slash(name="neko_ero", description="Too bad for catgirls...", guild_ids=guild_ids)
    async def _neko_ero(self, ctx):
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

    @cog_ext.cog_slash(name="classic_lewd", description="Classic lewd image.", guild_ids=guild_ids)
    async def _classic_lewd(self, ctx):
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

    @cog_ext.cog_slash(name="feet_lewd", description="You really love those bare feets, don't you?", guild_ids=guild_ids)
    async def _feet_lewd(self, ctx):
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