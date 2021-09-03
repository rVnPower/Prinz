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
import rule34
from pybooru import Danbooru
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


class Animensfw(commands.Cog, description="NSFW anime commands", name="➕"):
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

    @commands.command(description="Search for images on Rule34 with tags", aliases=['r34'])
    async def rule34(self, ctx, *, words:str):
        async def main(words):
            import rule34
            rule34 = rule34.Rule34(loop)
            r = await rule34.getImages(tags=words, randomPID=True)
            return r
        loop = asyncio.get_event_loop()
        if ctx.channel.is_nsfw():
            r = await main(words)
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_image(url=random.choice(r).file_url)
            embed.set_footer(text="If you are searching with a name, you should replace spaces with `_`")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('🔄')
            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji == '🔄', timeout=30.0)
                except asyncio.TimeoutError:
                    return
                else:
                    if reaction.emoji == '🔄':
                        embed = discord.Embed(colour=discord.Colour.blurple())
                        embed.set_image(url=random.choice(r).file_url)
                        embed.set_footer(text="If you are searching with a name, you should replace spaces with `_`")
                        await msg.edit(embed=embed)
                        await msg.remove_reaction('🔄', ctx.author)      
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="Get a random NSFW image of a topic")
    async def danbooru(self, ctx, *, words:str):
        if ctx.channel.is_nsfw():
            async def main(words):
                client = Danbooru('danbooru')
                r = client.post_list(tags=words, random=True)
                return r

            embed = discord.Embed(colour=discord.Colour.blurple())
            r = await main(words)
            post = random.choice(r)
            file_url = post['large_file_url']
            author = post['tag_string_artist']
            embed.set_author(name=F"Artist: {author}", url=post['source'])
            embed.set_image(url=file_url)
            embed.set_footer(text=post['tag_string_general'])
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('🔄')
            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji == '🔄', timeout=30.0)
                except asyncio.TimeoutError:
                    return
                else:
                    if reaction.emoji == '🔄':
                        embed = discord.Embed(colour=discord.Colour.blurple())
                        post = random.choice(r)
                        file_url = post['large_file_url']
                        author = post['tag_string_artist']
                        embed.set_author(name=author, url=post['source'])
                        embed.set_image(url=file_url)
                        embed.set_footer(text=post['tag_string_general'])
                        await msg.edit(embed=embed)
                        await msg.remove_reaction('🔄', ctx.author) 
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

    @commands.command(description="Get a bunch of NSFW anime images on HentaiZ")
    async def hentaiz(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

    @commands.command(description="Get a bunch of NSFW furry anime images on HentaiZ")
    async def hz_furry(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=622677550065516554', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

    @commands.command(description="Get a bunch of NSFW yuri anime images on HentaiZ")
    async def hz_yuri(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=616622475773476884', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

    @commands.command(description="Get a bunch of real life girls images on HentaiZ")
    async def hz_real(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=781870041862897684', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

def setup(bot):
	bot.add_cog(Animensfw(bot))