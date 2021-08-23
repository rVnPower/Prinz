#####################################################
import discord
from discord.ext import commands, tasks
import time
import nekos
import asyncio
from core.chat_formatting import bold, italics
#####################################################

class Simple(commands.Cog, description="Simple and fun commands"):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = time.time()

    @commands.command(name="hi", description="She will greet you!")
    async def _hi(self, ctx):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command(name="ping", description="Checks bot latency.")
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
        embed.add_field(name="Runtime: ", value=f'{round(h)} hour(s), {round(m)} minute(s), {round(s, 2)} second(s)', inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="admin", description="Display informations about bot owner.")
    async def _admin(self, ctx):
        # Prints infomation about the admin
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="VnPower!")
        embed.add_field(name='Website: ', value="[Here](https://page.vnpower.repl.co/)")
        embed.add_field(name='GitHub: ', value="[Here](https://github.com/rVnPower)")
        embed.add_field(name='Discord: ', value="VnPower#8888")
        await ctx.send(embed=embed)

    @commands.command(description="DM you a message")
    async def dm(self, ctx, *, words):
        await ctx.author.send(words)

    @commands.command(description="Get a random textcat")
    async def textcat(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.textcat)
        await ctx.send(r)

    @commands.command(description="Get a random fact")
    async def fact(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.fact)
        embed = discord.Embed(colour=discord.Colour.blurple(), title='Did you know?', description=nekos.fact)
        await ctx.send(embed=embed)

    @commands.command(description="Get a random cat image")
    async def cat(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.cat)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command(description="Get a random `why?` question")
    async def why(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.why)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=r.capitalize())
        await ctx.send(embed=embed)

    @commands.command(description="Answer your question with a random answer", aliases=['8ball'])
    async def eightball(self, ctx, *, words:str):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.eightball, words)
        if words.endswith('?'):
            embed = discord.Embed(colour=discord.Colour.blurple(), description=r.text.capitalize())
        else:
            embed = discord.Embed(colour=discord.Colour.blurple(), description="That does not look like a question.")
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Simple(bot))
