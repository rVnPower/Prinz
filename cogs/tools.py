#####################################################
import discord
from discord.ext import commands, tasks
import math
import random
import string
import requests
import json
import nekos
from core.chat_formatting import bold
#####################################################

class Tools(commands.Cog, description="Tools"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_content=True, description="Send a invite link")
    async def invite(self, ctx):
        await ctx.author.send("Here is the link! Thanks for inviting!\nhttps://discord.com/api/oauth2/authorize?client_id=877182587725049897&permissions=155118463095&scope=bot")

    @commands.command(hidden=True)
    async def ascii(self, ctx, *, words):
        await ctx.send(nekos.owoify(words))

    @commands.command(aliases=['owo'], description="Owoify a string! Nya~")
    async def owoify(self, ctx, *, words):
        await ctx.send(nekos.owoify(words))

    @commands.command(aliases=['av'], description="Show your avatar")
    async def avatar(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Avatar")
        embed.set_author(name=ctx.author)
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tools(bot))