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

class AnimeStuff(commands.Cog, description="Other stuff about anime"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Search for details of an anime charecter")
    async def ani_char(self, ctx, *, words):
        try:
            r = animec.sagasu.Charsearch(words)
        except animec.errors.NoResultsFound:
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Nothing found.")
            await ctx.send(embed=embed)
            return
        else:
            count = 0
            embed = discord.Embed(colour=discord.Colour.blurple(), title=r.title, url=r.url)
            embed.add_field(name="- ", value="References:")
            for i in r.references:
                count += 1
                embed.add_field(name=f"{count}.", value=f" {i}")
            embed.set_image(url=r.image_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ani_search'], description="Search for details of an anime movie")
    async def anime(self, ctx, *, words):
        seperator = ', '
        try:
            r = animec.anicore.Anime(words)
        except animec.errors.NoResultsFound:
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Nothing found.")
        else:
            current = 0
            embed = discord.Embed(colour=discord.Colour.blurple(), title=r.name, url=r.url)
            embed.add_field(name="English title: ", value=r.title_english)
            embed.add_field(name="Japanese title: ", value=r.title_jp)
            embed.add_field(name="Genres: ", value=seperator.join(r.genres))
            embed.add_field(name="Episodes: ", value=r.episodes)
            embed.add_field(name="Rank / Rating: ", value=f"{r.ranked} / {r.rating}")
            embed.add_field(name="Popularity: ", value=r.popularity)
            embed.add_field(name="NSFW: ", value=r.is_nsfw())
            embed.add_field(name="Also recommended: ", value=seperator.join(list(r.recommend())))
            embed.set_image(url=r.poster)
            await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(AnimeStuff(bot))