#####################################################
import discord
from discord.ext import commands, tasks
import time
import nekos
import asyncio
import aiohttp
import random
import json
import string
from core.chat_formatting import bold, italics
from core.mem_profile import memory_usage_resource
#####################################################
async def get_prefix(bot, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        prefixes[str(message.guild.id)] = 'l!'

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        return prefixes[str(message.guild.id)]

class Simple(commands.Cog, description="Funny, simple and useless commands", name="Simple"):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = time.time()

    @commands.command(name="hi", help="She will greet you!")
    async def _hi(self, ctx):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command(name="ping", help="Checks bot latency.")
    async def _ping(self, ctx):
        # Checks bot latency
        t2 = time.time()
        n = t2-self.t1
        h = n // 3600
        s = n % 3600
        m = s // 60
        s = s % 60
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Pong! {p}ms!')
        embed.add_field(name="Runtime: ", value=f"{round(h)} hour{'s' if h > 1 else ''}, {round(m)} minute{'s' if round(m) > 1 else ''}, {round(s)} second{'s' if round(s) > 1 else ''}", inline=True)
        embed.add_field(name="Memory used: ", value=f"{memory_usage_resource()} MB")
        await ctx.send(embed=embed)

    @commands.command(help="Display informations about this bot.")
    async def info(self, ctx):
        # Prints infomation about the admin
        embed = discord.Embed(colour=discord.Colour.blurple(), description="Prinz is a simple Discord bot that was made for informations and anime. I do not want this bot to grow for now, because of Discord bad decisions.")
        embed.set_footer(text="Made from ❤️ | VnPower#8888", icon_url="https://cdn.discordapp.com/avatars/683670893515636749/7d8f6a81109fcc1c4afe451495b848e5.webp?size=1024")
        embed.add_field(name=f"{await get_prefix(self.bot, ctx)}help: ", value="For help", inline=True)
        embed.add_field(name=f"{await get_prefix(self.bot, ctx)}invite: ", value="DM you an invite link", inline=True)
        embed.add_field(name="Support us?", value="Vote for the bot: ")
        await ctx.send(embed=embed)

    @commands.command(help="DM you a message")
    async def dm(self, ctx, *, words):
        await ctx.author.send(words)

    @commands.command(help="Get a random textcat", aliases=['kao'])
    async def textcat(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.textcat)
        await ctx.send(r)

    @commands.command(help="Get a random fact")
    async def fact(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.fact)
        embed = discord.Embed(colour=discord.Colour.blurple(), title='Did you know?', description=r)
        await ctx.send(embed=embed)

    @commands.command(help="Get a random cat")
    async def cat(self, ctx):
        phrase = ['Meow!', 'Grrrr...', 'Nya~']
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.cat)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        embed.set_footer(text=random.choice(phrase))
        await ctx.send(embed=embed)

    @commands.command(help="Get a random `why?` question")
    async def why(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.why)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=r.capitalize())
        await ctx.send(embed=embed)

    @commands.command(help="Answer your question with a random answer", aliases=['8ball'])
    async def eightball(self, ctx, *, words:str):
        print(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.eightball)
        if words.endswith('?'):
            embed = discord.Embed(colour=discord.Colour.blurple(), description=r.text.capitalize())
        else:
            embed = discord.Embed(colour=discord.Colour.blurple(), description="That does not look like a question.")
        await ctx.send(embed=embed)

    @commands.command(help="Get a random dog")
    async def dog(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_footer(text="Source: https://dog.ceo/api/breeds/image/random")
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://dog.ceo/api/breeds/image/random') as resp:
                print(resp.status)
                if int(resp.status) != 200:
                    embed.set_author(name="The server does not respond... Maybe try again later.")
                    await ctx.send(embed=embed)
                    return
                r = await resp.json()
        embed.set_author(name="Woof!")
        embed.set_image(url=r['message'])
        await ctx.send(embed=embed)

    @commands.command(help="Get a random duck")
    async def duck(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_footer(text="Source: https://random-d.uk/api/random?format=json")
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://random-d.uk/api/random?format=json') as resp:
                if int(resp.status) != 200:
                    embed.set_author(name="The server does not respond... Maybe try again later.")
                    await ctx.send(embed=embed)
                    return
                r = await resp.json()
        embed.set_author(name="Quack!")
        embed.set_image(url=r['url'])
        await ctx.send(embed=embed)

    @commands.command(help="Emojify")
    async def emojify(self, ctx, *, words:str):
        emojis = []
        for s in words.lower():
            if s.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two',
                            '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emoji.append(s)
        await ctx.send(''.join(emojis))


def setup(bot):
	bot.add_cog(Simple(bot))
