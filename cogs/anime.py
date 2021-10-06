#####################################################
import discord
from discord.ext import commands, tasks
import random

import animec
import asyncio
import aiohttp
from bs4 import BeautifulSoup

from utils.requests import get_requests_as_json, get_requests_as_text
from discord.ext.commands.cooldowns import BucketType
#####################################################

class Anime(commands.Cog, description="For weebs", name="Anime"):
    def __init__(self, bot):
        self.bot = bot
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Send a random illustration from my owner's Google Drive")
    async def sfw(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/G-Rated/{random.randint(1,145)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Send a random ecchi illustration from my owner's Google Drive")
    async def ecchi(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/Ecchi/{random.randint(1,82)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Send a random waifu")
    async def waifu(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.waifu)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
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
                    r = await loop.run_in_executor(None, animec.waifu.Waifu.waifu)
                    embed.set_image(url=r)
                    await msg.edit(embed=embed)
                    await msg.remove_reaction('🔄', ctx.author)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Send a random catgirl illustration")
    async def neko(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.neko)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Send a random anime GIF")
    async def randomGif(self, ctx):
        r = animec.waifu.Waifu.random_gif()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Get a bunch of SFW illustration on HentaiZ")
    async def hz_anime(self, ctx, page:int=random.randint(1, 200)):
        r = await get_requests_as_text()
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

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Kiss someone")
    async def kiss(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.kiss)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} kissed {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Hug someone")
    async def hug(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.hug)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hugged {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Cuddle someone")
    async def cuddle(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.cuddle)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cuddled {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Cry ;_;")
    async def cry(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.cry)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cried!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Blush #._.# ")
    async def blush(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.blush)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} blushed!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Smile :)")
    async def smile(self, ctx):
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.smile)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} smiled!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Pat someone")
    async def pat(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.pat)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} patted {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Lick somebody")
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

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Bite somebody")
    async def bite(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bit)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bit {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Handhold somebody")
    async def handhold(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.handhold)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hand-held {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Slap somebody")
    async def slap(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.slap)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} slapped {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Bonk somebody")
    async def bonk(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bonk)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bonked {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Poke somebody")
    async def poke(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.poke)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} poked {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Kill somebody")
    async def kill(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.kill)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} killed {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Bully somebody")
    async def bully(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.bully)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bullied {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(help="Highfive with somebody")
    async def highfive(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, animec.waifu.Waifu.highfive)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} high-fived with {mem.split('#')[0]}!")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(help="Search for details of an anime charecter")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ani_char(self, ctx, *, words):
        loop = asyncio.get_event_loop()
        try:
            r = await loop.run_in_executor(None, animec.sagasu.Charsearch, words)
        except animec.NoResultFound:
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Nothing found.")
            await ctx.send(embed=embed)
            return
        else:
            count = 0
            embed = discord.Embed(colour=discord.Colour.blurple(), title=r.title, url=r.url)
            embed.add_field(name="- ", value="References:")
            for i in r.references:
                count += 1
                embed.add_field(name=f"{count}.", value=f" {i}")
            embed.set_image(url=r.image_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ani_search'], help="Search for details of an anime movie")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def anime(self, ctx, *, words):
        seperator = ', '
        loop = asyncio.get_event_loop()
        try:
            r = await loop.run_in_executor(None, animec.anicore.Anime, words)
        except animec.errors.NoResultsFound:
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Nothing found.")
        else:
            current = 0
            embed = discord.Embed(colour=discord.Colour.blurple(), title=r.name, url=r.url)
            embed.add_field(name="English title: ", value=r.title_english)
            embed.add_field(name="Japanese title: ", value=r.title_jp)
            embed.add_field(name="Genres: ", value=seperator.join(r.genres))
            embed.add_field(name="Episodes: ", value=r.episodes)
            embed.add_field(name="Rank / Rating: ", value=f"{r.ranked} / {r.rating}")
            embed.add_field(name="Popularity: ", value=r.popularity)
            embed.add_field(name="NSFW: ", value=r.is_nsfw())
            embed.add_field(name="Also recommended: ", value=seperator.join(list(r.recommend())))
            embed.set_image(url=r.poster)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))
