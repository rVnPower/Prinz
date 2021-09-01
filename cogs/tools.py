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
import asyncio
import re
#####################################################

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

async def convert(self, ctx, argument):
    time_regex = re.compile(r"(\d{1,5}(?:[.,]?\d{1,5})?)([smhd])")
    time_dict = {"h":3600, "s":1, "m":60, "d":86400}
    matches = time_regex.findall(argument.lower())
    time = 0
    for v, k in matches:
        try:
            time += time_dict[k]*float(v)
        except KeyError:
            embed = discord.Embed(color = discord.Colour.blurple(),description=  "{} is an invalid time-key! h/m/s/d are valid!".format(k))
            await ctx.send(embed=embed)
    return time

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
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.owoify, words)
        await ctx.send(r)

    @commands.command(aliases=['av'], description="Show your avatar")
    async def avatar(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Avatar")
        embed.set_author(name=ctx.author)
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description="Create a simple poll")
    async def poll(self, ctx, time:str = '30m', *, topic:str):
        embed = discord.Embed(title=f"{ctx.author} asks: {topic}", description=f":one: Yes\n:two: No", color = discord.Colour.blurple())

        time = await convert(self, ctx, time)
        h = round(time) // 3600
        s = round(time) % 3600
        m = s // 60
        s = s % 60

        embed.add_field(name="Duration: ", value=f"{h} hour{'s' if h > 1 else ''}, {m} minute{'s' if m > 1 else ''}, {s} second{'s' if s > 1 else ''}")
        embed.set_footer(text= f"Poll created at {ctx.message.created_at}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        try:
            await ctx.message.delete()
        except:
            pass
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')

        await asyncio.sleep(time)

        newMSG = await ctx.fetch_message(msg.id)
        onechoice = await newMSG.reactions[0].users().flatten()
        secchoice = await newMSG.reactions[1].users().flatten()

        result = "Tie"
        if len(onechoice) > len(secchoice):
            result = 'Yes'
        elif len(secchoice) > len(onechoice):
            result = 'No'

        embed = discord.Embed(title=topic, description=f"Result: {result}", color = discord.Colour.blurple())
        await newMSG.edit(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def quickpoll(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly.
        The first argument is the question and the rest are the choices.
        """

        if len(questions_and_choices) < 3:
            embed = discord.Embed(colour=discord.Colour.blurple(), description="Need at least 1 question with 2 choices.")
            return await ctx.send(embed=embed)
        elif len(questions_and_choices) > 21:
            embed = discord.Embed(colour=discord.Colour.blurple(), description="You can only have up to 20 choices.")
            return await ctx.send(embed=embed)

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        embed = discord.Embed(colour=discord.Colour.blurple(), title=f"{ctx.author} asks: {question}\n\n", description=body)
        embed.set_footer(text= f"Poll created at {ctx.message.created_at}", icon_url=ctx.author.avatar_url)
        poll = await ctx.send(embed=embed)
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

def setup(bot):
    bot.add_cog(Tools(bot))