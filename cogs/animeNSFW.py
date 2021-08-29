#####################################################
import discord
from discord.ext import commands, tasks
import random
import json
from NHentai.nhentai import NHentai
import animec
import asyncio
import nekos
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json
#####################################################
possible = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
        'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
        'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
        'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
        'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
        'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
        'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
        ]


class Animensfw(commands.Cog, description="NSFW anime commands"):
    def __init__(self, bot):
        self.bot = bot
        self.possible = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
        'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
        'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
        'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
        'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
        'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
        'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
        ]
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    @commands.command(description="Send a random hentai image")
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

    @commands.command(description="Too bad for catgirls...", aliases=['nE'])
    async def neko_ero(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.nekos.dev/api/v3/images/nsfw/img/neko_ero/') as resp:
                r = await resp.json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="Classic lewd image.", aliases=['cL'])
    async def classic_lewd(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.nekos.dev/api/v3/images/nsfw/img/classic_lewd/') as resp:
                r = await resp.json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            await ctx.send(embed=embed)
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="You really love those bare feets, don't you?", aliases=['fL'])
    async def feet_lewd(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.nekos.dev/api/v3/images/nsfw/img/feet_lewd/') as resp:
                r = await resp.json()
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='Here is your image!')
            embed.set_image(url=data['data']['response']['url'])
            await ctx.send(embed=embed)
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="Get a random NSFW image of a topic")
    async def lewd(self, ctx, *, words:str = random.choice(possible)):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_image(url=nekos.img(words))
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
        await ctx.send(embed=embed)

    @commands.command(description="Get a bunch of images on HentaiZ")
    async def hentaiz(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

def setup(bot):
	bot.add_cog(Animensfw(bot))