#####################################################
import discord
from discord.ext import commands, tasks

import random

from NHentai.nhentai import NHentai

import asyncio
import nekos
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json
import rule34
from pybooru import Danbooru

from discord.ext.commands.cooldowns import BucketType
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


class Animensfw(commands.Cog, description="NSFW anime commands", name="Anime NSFW"):
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

    @commands.command(help="Send a random hentai image")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(help="Search for images on Rule34 with tags", aliases=['r34'])
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(help="Get a random NSFW image of a topic")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(help="Get a random NSFW image of a topic")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lewd(self, ctx, *, words:str = random.choice(possible)):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_image(url=nekos.img(words))
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
        await ctx.send(embed=embed)

    @commands.command(help="Get a bunch of NSFW anime images on HentaiZ")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hentaiz(self, ctx, page:int=random.randint(1, 200)):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://hentaiz.cc/gallery/page/{page}', headers=self.headers) as resp:
                    r = await resp.text()
                    soup = BeautifulSoup(r, 'lxml')
                    links = []
                    for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                        links.append(img['data-mdb-img'])
                        if len(links) > 4:
                            await ctx.send('\n'.join(links))
                            links.clear()
                            asyncio.sleep(2)
                    try:
                        await ctx.send('\n'.join(links))
                    except:
                        pass
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(help="Get a bunch of NSFW furry anime images on HentaiZ")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hz_furry(self, ctx, page:int=random.randint(1, 200)):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=622677550065516554', headers=self.headers) as resp:
                    r = await resp.text()
                    soup = BeautifulSoup(r, 'lxml')
                    links = []
                    for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                        links.append(img['data-mdb-img'])
                        if len(links) > 4:
                            await ctx.send('\n'.join(links))
                            links.clear()
                            asyncio.sleep(2)
                    try:
                        await ctx.send('\n'.join(links))
                    except:
                        pass
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(help="Get a bunch of NSFW yuri anime images on HentaiZ")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hz_yuri(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=616622475773476884', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                links = []
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    links.append(img['data-mdb-img'])
                    if len(links) > 4:
                        await ctx.send('\n'.join(links))
                        links.clear()
                        asyncio.sleep(2)
                try:
                    await ctx.send('\n'.join(links))
                except:
                    pass

    @commands.command(help="Get a bunch of real life girls images on HentaiZ")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hz_real(self, ctx, page:int=random.randint(1, 200)):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B%5D=781870041862897684', headers=self.headers) as resp:
                    r = await resp.text()
                    soup = BeautifulSoup(r, 'lxml')
                    links = []
                    for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                        links.append(img['data-mdb-img'])
                        if len(links) > 4:
                            await ctx.send('\n'.join(links))
                            links.clear()
                            asyncio.sleep(2)
                    try:
                        await ctx.send('\n'.join(links))
                    except:
                        pass
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(aliases=['rD'], description="Get a random doujin on NHentai")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def random_doujin(self, ctx):
        if ctx.channel.is_nsfw():
            nhentai_async = NHentai.NHentaiAsync()
            Doujin = await nhentai_async.get_random()
            embed = discord.Embed(colour=discord.Colour.blurple(), title=Doujin.title, url=f'https://nhentai.net/g/{Doujin.id}', description=f"ID: {Doujin.id}")
            embed.set_image(url=Doujin.images[0])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="Search for doujin on NHentai")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def search_doujin(self, ctx, *, words:int):
        current = 0
        nhentai = NHentai()
        SearchPage = nhentai.search(query='naruto', sort='popular', page=1)
        Doujin = SearchPage.doujins[0]
        embed = discord.Embed(color=discord.colour.blurple(), title=Doujin.title, url=f'https://nhentai.net/g/{Doujin.id}')
        embed.set_image(url=Doujin.cover)

        # Start looping
        current = 0
        # Add reactions and do stuff
        buttons = ['⏪', '◀️', '▶️', '⏩']
        msg = await ctx.send(embed=embeds[current])
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Time out!")
                return
            else:
                previous_page = current
                if reaction.emoji == '⏪':
                    current = 0
                elif reaction.emoji == '◀️':
                    if current > 0:
                        current -= 1
                    else:
                        current = len(embeds) - 1
                elif reaction.emoji == '▶️':
                    if current < len(embeds):
                        current += 1
                    else:
                        current = 0
                elif reaction.emoji == '⏩':
                    current = len(embeds) - 1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                    if current != previous_page:
                        await msg.edit(embed=embeds[current])

    @commands.command(description="Read a doujin on NHentai")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def read_doujin(self, ctx, *, words:int):
        current = 0
        nhentai = NHentai()
        Doujin = nhentai.get_doujin(id=words)
        embeds = []
        # Start looping
        for i in Doujin.images:
            current +=1
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name=f"Page {current}/{len(Doujin.images)-1}")
            embed.set_image(url=i)
            embeds.append(embed)
        current = 0
        # Add reactions and do stuff
        buttons = ['⏪', '◀️', '▶️', '⏩']
        msg = await ctx.send(embed=embeds[current])
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Time out!")
                return
            else:
                previous_page = current
                if reaction.emoji == '⏪':
                    current = 0
                elif reaction.emoji == '◀️':
                    if current > 0:
                        current -= 1
                    else:
                        current = len(embeds) - 1
                elif reaction.emoji == '▶️':
                    if current < len(embeds):
                        current += 1
                    else:
                        current = 0
                elif reaction.emoji == '⏩':
                    current = len(embeds) - 1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                    if current != previous_page:
                        await msg.edit(embed=embeds[current])

def setup(bot):
	bot.add_cog(Animensfw(bot))