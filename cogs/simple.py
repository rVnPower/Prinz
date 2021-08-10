#####################################################
import discord
from discord.ext import commands, tasks
import time
#####################################################

class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = time.time()

    @commands.command(name="help", description="If you need help.")
    async def _help(self, ctx):
        # Help
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='Announcement!')
        embed.add_field(name='I am still developing this bot!', value='There will be a website for this bot... So stay tuned!')
        await ctx.send(embeds=[embed])

    @commands.command(name="hi", description="She will greet you!")
    async def _hi(self, ctx):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command(name="ping", description="Checks bot latency.")
    async def _ping(self, ctx):
        # Checks bot latency
        t2 = time.time()
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Pong! {p}ms!')
        embed.add_field(name="Runtime: ", value=f'{round(t2-self.t1, 2)} seconds', inline=True)
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

    @commands.command()
    async def dm(self, ctx, *, words):
        await ctx.author.send(words)

def setup(bot):
	bot.add_cog(Simple(bot))
