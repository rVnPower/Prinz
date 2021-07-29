#####################################################
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import wikipedia
from saucenao_api import SauceNao
import requests
import json
#####################################################
payload={}
headers = {}
response = requests.request("GET", "https://api.covid19api.com/summary", headers=headers, data=payload)
covi = response.json()

class Infomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='Help Command')
        # embed.add_field(name='.pixiv', value='Returns a VnPower approved Pixiv link!')
        embed.add_field(name='l!clear <int>',
                        value='Delete a number of messenges.')
        embed.add_field(name='l!ping', value='Check the bot latency.')
        embed.add_field(name='l!kick <member> <reason>', value='Kick a member!')
        embed.add_field(name='l!ban <member> <reason>',
                        value='Ban a member! Unban is under working!')
        embed.add_field(name='l!hi', value='Say hi!')
        await ctx.send(embed=embed)


    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f'Hi! {ctx.author.mention}')


    @commands.command()
    async def ping(self, ctx):
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Pong! {p}ms!')
        await ctx.send(embed=embed)

    @commands.command()
    async def admin(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="VnPower!")
        embed.add_field(name='Website: ', value="")
        embed.add_field(name='GitHub: ', value="")
        embed.add_field(name='Discord: ', value="")
        await ctx.send(embed=embed)

    @commands.command()
    async def wiki(self, ctx, *, words):
        await ctx.send(wikipedia.summary(words, features="lxml"))

    @commands.command()
    async def sauce(self, ctx, *, words):
        sauce = SauceNao('18007b616a0808aa80ae9e17e3a8d110e53b081c')
        results = sauce.from_url(words)  # or from_file()

        best = results[0]
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=best.title)
        embed.add_field(name="Link:  [Here](best.urls[1])", value=f"[{best.urls[1]}]")
        await ctx.send(embed=embed)

    @commands.command()
    async def covid(self, ctx, *, words):
        global covi
        newConfirmed = 0
        totalConfirmed= 0
        newDeaths = 0
        totalDeaths= 0
        newRecovered = 0
        totalRecovered= 0
        for i in covi['Countries']:
            if str(i['Country'].lower()) == str(words.lower()) or str(i['CountryCode'].lower()) == str(words.lower()):
                newConfirmed = i['NewConfirmed']
                totalConfirmed= i['TotalConfirmed']
                newDeaths = i['NewDeaths']
                totalDeaths= i['TotalDeaths']
                newRecovered = i['NewRecovered']
                totalRecovered= i['TotalRecovered']
                embed = discord.Embed(colour=discord.Colour.blurple())
                embed.set_author(name=f"Covid-19 stats in {i['Country']}({i['CountryCode']})!")
                embed.add_field(name="New comfirmed:", value=newConfirmed)
                embed.add_field(name="Total comfirmed:", value=totalConfirmed)
                embed.add_field(name="New deaths:", value=newDeaths)
                embed.add_field(name="Total deaths:", value=totalDeaths)
                embed.add_field(name="New recovered:", value=newRecovered)
                embed.add_field(name="Total recovered:", value=totalRecovered)
                await ctx.send(embed=embed)
                break

    @commands.command(aliases=[])
    async def countries(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Country names and country codes(ISO Alpha-2)")
        embed.add_field(name=".", value='var.countries')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Infomation(bot))