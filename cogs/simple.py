#####################################################
import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
#####################################################

class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", description="If you need help.")
    async def _help(self, ctx: SlashContext):
        # Help
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='Announcement!')
        embed.add_field(name='I am still developing this bot!', value='There will be a website for this bot... So stay tuned!')
        await ctx.send(embeds=[embed])

    @commands.command(name="hi", description="She will greet you!")
    async def _hi(self, ctx: SlashContext):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command(name="ping", description="Checks bot latency.")
    async def _ping(self, ctx: SlashContext):
        # Checks bot latency
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Pong! {p}ms!')
        await ctx.send(embed=embed)

    @commands.command(name="admin", description="Display informations about bot owner.")
    async def _admin(self, ctx: SlashContext):
        # Prints infomation about the admin
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="VnPower!")
        embed.add_field(name='Website: ', value="[Here](https://page.vnpower.repl.co/)")
        embed.add_field(name='GitHub: ', value="-")
        embed.add_field(name='Discord: ', value="-")
        await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Simple(bot))