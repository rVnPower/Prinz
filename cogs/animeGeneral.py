#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
from NHentai.nhentai import NHentai
import animec
import asyncio
import aiohttp
from bs4 import BeautifulSoup
#####################################################

class Anime(commands.Cog, description="General anime commands", name="➕"):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    @commands.command(description="Send a random anime image from VnPower's Google Drive")
    async def sfw(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/G-Rated/{random.randint(1,145)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command(description="Send a random ecchi image")
    async def ecchi(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/Ecchi/{random.randint(1,82)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command(description="Send a random waifu")
    async def waifu(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.waifu)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Send a random catgirl pic")
    async def neko(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.neko)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Send a random anime GIF")
    async def randomGif(self,ctx):
        r = animec.waifu.Waifu.random_gif()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Get a bunch of anime images on HentaiZ")
    async def hz_anime(self, ctx, page:int=random.randint(1, 200)):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://hentaiz.cc/gallery/page/{page}/?channels%5B0%5D=616622316356501515', headers=self.headers) as resp:
                r = await resp.text()
                soup = BeautifulSoup(r, 'lxml')
                for img in soup.findAll('img', class_="lazyload img-fluid mb-2 shadow-5-strong rounded"):
                    await ctx.send(img['data-mdb-img'])

    @commands.command(description="Kiss an user")
    async def kiss(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.kiss)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} kissed {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Hug an user")
    async def hug(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.hug)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hugged {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Cuddle an user")
    async def cuddle(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.cuddle)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cuddled {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Cry ;_;")
    async def cry(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.cry)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cried!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Blush #._.# ")
    async def blush(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.blush)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} blushed!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Smile :)")
    async def smile(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.smile)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} smiled!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Pat an user")
    async def pat(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.pat)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} patted {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Lick an user")
    async def lick(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.lick)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} licked {mem.split('#')[0]}!")
        embed.set_image(url=r)
        embed.set_footer(text="Eww.")
        await ctx.send(embed=embed)

    @commands.command(description="Bite an user")
    async def bite(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bit)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bit {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Handhold an user")
    async def handhold(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.handhold)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hand-held {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Slap an user")
    async def slap(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.slap)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} slapped {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Bonk an user")
    async def bonk(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bonk)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bonked {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Poke an user")
    async def poke(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.poke)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} poked {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Kill an user")
    async def kill(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.kill)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} killed {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Bully an user")
    async def bully(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bully)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bullied {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Highfive with an user")
    async def highfive(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.highfive)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} high-fived with {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))