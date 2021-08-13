#####################################################
import discord
from discord.ext import commands, tasks
import math
import PIL.Image
import random
import string
import requests
import json

from core.chat_formatting import bold
#####################################################

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_content=True)
    async def invite(self, ctx):
        await ctx.author.send("Here is the link! Thanks for inviting!\nhttps://discord.com/api/oauth2/authorize?client_id=865487746905931846&permissions=140056586310&scope=bot%20applications.commands")

    @commands.command()
    async def ascii(self, ctx, *, words):
        await ctx.send(bold('Hi'))

    @commands.command(aliases=['av'])
    async def avatar(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Avatar")
        embed.set_author(name=ctx.author)
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tools(bot))