#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
from NHentai.nhentai import NHentai
import animec
#####################################################

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomImg", description="Send a random image", aliases=['rI'])
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

    @commands.command(name="img", description="Send a random anime image from VnPower's GDrive")
    async def _img(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/G-Rated/{random.randint(1,145)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command(name="ecchi", description="Send a random ecchi image")
    async def _ecchi(self, ctx):
      url = f'https://raw.githubusercontent.com/rVnPower/LewdPower/master/Yes/Ecchi/{random.randint(1,82)}.jpg'
      embed = discord.Embed(colour=discord.Colour.blurple())
      embed.set_author(name='Here is your image!')
      embed.set_image(url=url)
      await ctx.send(embed=embed)

    @commands.command(name="hentai", description="Send a random hentai image")
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

    @commands.command(name="nekoEro", description="Too bad for catgirls...", aliases=['nE'])
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

    @commands.command(name="classicLewd", description="Classic lewd image.", aliases=['cL'])
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

    @commands.command(name="feetLewd", description="You really love those bare feets, don't you?", aliases=['fL'])
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

    @commands.command(aliases=['rD'])
    async def random_doujin(self ,ctx):
        if ctx.channel.is_nsfw():
            nhentai = NHentai()
            Doujin = nhentai.get_random()
            embed = discord.Embed(colour=discord.Colour.blurple(), title=Doujin.title, url=f'https://nhentai.net/g/{Doujin.id}')
            embed.set_image(url=Doujin.images[0])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} kissed {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.kiss())
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} hugged {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.hug())
        await ctx.send(embed=embed)

    @commands.command()
    async def cuddle(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cuddled {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.cuddle())
        await ctx.send(embed=embed)

    @commands.command()
    async def cry(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} cried!")
        embed.set_image(url=animec.waifu.Waifu.cry())
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} patted {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.pat())
        await ctx.send(embed=embed)

    @commands.command()
    async def lick(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} licked {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.lick())
        embed.set_footer(text="Eww.")
        await ctx.send(embed=embed)

    @commands.command()
    async def bite(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} bit {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.bite())
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} slapped {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.slap())
        await ctx.send(embed=embed)

    @commands.command()
    async def poke(self, ctx, member:discord.Member):
        mem = str(member)
        author = str(ctx.author)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"{author.split('#')[0]} poked {mem.split('#')[0]}!")
        embed.set_image(url=animec.waifu.Waifu.poke())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Anime(bot)) 