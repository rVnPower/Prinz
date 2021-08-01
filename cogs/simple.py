#####################################################
import discord
from discord.ext import commands, tasks
#####################################################

class Simple(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
    @commands.command()
    async def help(self, ctx):
        # Help
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='Announcement!')
        embed.add_field(name='I am still developing this bot!', value='There will be a website for this bot... So stay tuned!')
        await ctx.send(embed=embed)

    @commands.command()
    async def hi(self, ctx):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command()
    async def ping(self, ctx):
        # Checks bot latency
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Pong! {p}ms!')
        await ctx.send(embed=embed)

    @commands.command()
    async def admin(self, ctx):
        # Prints infomation about the admin
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="VnPower!")
        embed.add_field(name='Website: ', value="[Here](https://page.vnpower.repl.co/)")
        embed.add_field(name='GitHub: ', value="-")
        embed.add_field(name='Discord: ', value="-")
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Simple(bot))