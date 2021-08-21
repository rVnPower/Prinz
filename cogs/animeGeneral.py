#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
from NHentai.nhentai import NHentai
import animec
import asyncio
#####################################################

class Anime(commands.Cog, description="General anime commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Send a random anime image from VnPower's GDrive")
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
        r = animec.waifu.Waifu.waifu()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Send a random catgirl pic")
    async def neko(self, ctx):
        r = animec.waifu.Waifu.neko()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Send a random anime GIF")
    async def randomGif(self,ctx):
        r = animec.waifu.Waifu.random_gif()
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Kiss an user")
    async def kiss(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} kissed {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.kiss())
        await ctx.send(embed=embed)

    @commands.command(description="Hug an user")
    async def hug(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hugged {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.hug())
        await ctx.send(embed=embed)

    @commands.command(description="Cuddle an user")
    async def cuddle(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cuddled {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.cuddle())
        await ctx.send(embed=embed)

    @commands.command(description="Cry ;_;")
    async def cry(self, ctx):
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cried!")
        embed.set_image(url=animec.waifu.Waifu.cry())
        await ctx.send(embed=embed)

    @commands.command(description="Blush #._.# ")
    async def blush(self, ctx):
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} blushed!")
        embed.set_image(url=animec.waifu.Waifu.blush())
        await ctx.send(embed=embed)

    @commands.command(description="Smile :)")
    async def smile(self, ctx):
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} smiled!")
        embed.set_image(url=animec.waifu.Waifu.blush())
        await ctx.send(embed=embed)

    @commands.command(description="Pat an user")
    async def pat(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} patted {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.pat())
        await ctx.send(embed=embed)

    @commands.command(description="Lick an user")
    async def lick(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} licked {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.lick())
        embed.set_footer(text="Eww.")
        await ctx.send(embed=embed)

    @commands.command(description="Bite an user")
    async def bite(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bit {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.bite())
        await ctx.send(embed=embed)

    @commands.command(description="Handhold an user")
    async def handhold(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hand-held {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.handhold())
        await ctx.send(embed=embed)

    @commands.command(description="Slap an user")
    async def slap(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} slapped {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.slap())
        await ctx.send(embed=embed)

    @commands.command(description="Bonk an user")
    async def bonk(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bonked {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.slap())
        await ctx.send(embed=embed)

    @commands.command(description="Poke an user")
    async def poke(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} poked {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.poke())
        await ctx.send(embed=embed)

    @commands.command(description="Kill an user")
    async def kill(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} killed {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.kill())
        await ctx.send(embed=embed)

    @commands.command(description="Bully an user")
    async def bully(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bullied {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.poke())
        await ctx.send(embed=embed)

    @commands.command(description="Highfive with an user")
    async def highfive(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} high-fived with {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.highfive())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot))