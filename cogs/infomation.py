#####################################################
import discord
from discord.ext import commands, tasks
import random
import wikipedia
import aiohttp
import json
import asyncio
import wolframalpha
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import os
from dotenv import load_dotenv
#####################################################

class Information(commands.Cog, description="Information commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['whois', 'info'], description='Check an user infomation.')
    async def wis(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Infomation of {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='ID:' ,value=member)
        embed.add_field(name='Nickname: ',value=member.display_name)
        embed.add_field(name= 'Joined on: ', value= member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name= 'Joined server on: ', value= member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name= f"Roles: ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name= "Highest role: ",value=member.top_role.mention)
        await ctx.send(embed=embed)

    @commands.command(description="Check your Discord account details")
    async def whoami(self, ctx):
        roles = [role for role in ctx.author.roles]
        embed = discord.Embed(colour=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Infomation of {ctx.author}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='ID:' ,value=ctx.author)
        embed.add_field(name='Nickname: ',value=ctx.author.display_name)
        embed.add_field(name= 'Joined on: ', value= ctx.author.created_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name= 'Joined server on: ', value= ctx.author.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name= f"Roles: ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name= "Highest role: ",value=ctx.author.top_role.mention)
        await ctx.send(embed=embed)


    @commands.command(name="weather", description="Checks weather in a location.")
    async def _weather(self, ctx, *, words:str):
        # Weather
        owm = OWM('081c82065cfee62cb7988ddf90914bdd')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(words)
        w = observation.weather
        if 0 <= w.wind()['deg'] < 90:direction = 'N'
        if 90 <= w.wind()['deg'] < 180:direction = 'E'
        if 180 <= w.wind()['deg'] < 270:direction = 'S'
        if 270 <= w.wind()['deg'] < 360:direction = 'W'

        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"Weather stats in {words}!")
        embed.add_field(name="Status:", value=w.detailed_status)
        embed.add_field(name="Wind Speed:", value=f"{w.wind()['speed']}km/h {direction}")
        embed.add_field(name="Wind Degree:", value=w.wind()['deg'])
        embed.add_field(name="Humidity:", value=w.humidity)
        embed.add_field(name="Max. temperature:", value=f"{w.temperature('celsius')['temp_max']}°C /{w.temperature('fahrenheit')['temp_max']}°F")
        embed.add_field(name="Average temperature: ", value=f"{w.temperature('celsius')['temp']}°C /{w.temperature('fahrenheit')['temp']}°F")
        embed.add_field(name="Rain:", value=w.rain)
        embed.add_field(name="Clouds:", value=w.clouds)
        await ctx.send(embed=embed)

    @commands.command(name= "wikilan", description="Changes Wikipedia 's language.")
    async def _wikilan(self, ctx, *, Pinput:str):
        # Changes Wikipedia language
        embed = discord.Embed(colour=discord.Colour.blurple())
        if Pinput.lower().strip() in wikipedia.languages():
            wikipedia.set_lang(Pinput)
            embed.set_author(name=f"Changed Wikipedia's language to {wikipedia.languages()[Pinput.lower()]}({Pinput.upper()})!")
            await ctx.send(embed=embed)
        else:
            embed.set_author(name=f'That language does not exist in Wikipedia!')
            await ctx.send(embed=embed)

    @commands.command(name="wiki", description="Searches articles on Wikipedia")
    # Searches articles on Wikipedia
    async def wiki(self, ctx, *, Pinput:str):
        # Searches Wikipedia
        lis = []
        count = 1
        searchR = wikipedia.search(Pinput)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f"Search results of {Pinput} on Wikipedia:")
        embed.set_footer(text="Type 'cancel' to abort.")
        for i in searchR:
            li = {}
            embed.add_field(name=f"{count}. ", value=i, inline=True)
            li['id'] = count
            li['name'] = i
            lis.append(li)
            count +=1
        await ctx.send(embed=embed)
        while True:
            def is_correct(m):
                return m.author == ctx.author

            embed = discord.Embed(colour=discord.Colour.blurple())
            try:
                pinput = await self.bot.wait_for('message', check=is_correct, timeout=30.0)
            except asyncio.TimeoutError:
                embed.set_author(name=f'Time out!')
                await ctx.send(embed=embed)
                break
            try:
                if 1 <= int(pinput.content) <= 10:
                    for i in lis:
                        if int(i['id']) == int(pinput.content):
                            name = i['name']
                            embed.set_author(name=f'Summary of {name}')
                            embed.add_field(name=name, value=wikipedia.summary(name, sentences=3))
                            await ctx.send(embed=embed)
                            return None
            except ValueError:
                if str(pinput.content).lower().strip() == 'cancel':
                    embed.set_author(name='Canceled!')
                    await ctx.send(embed=embed)
                    break
        await ctx.send(embed=embed)

    @commands.command(name="sauce", description="Find an image source.")
    async def _sauce(self, ctx, *, words:str):
        from pysaucenao import SauceNao, PixivSource, VideoSource, MangaSource
        sauce = SauceNao(api_key='18007b616a0808aa80ae9e17e3a8d110e53b081c')

        # results = await sauce.from_file('/path/to/image.png')
        results = await sauce.from_url(words)
        best = results[0]
        embed = discord.Embed(colour=discord.Colour.blurple(), title=best.author_name, url=best.author_url)
        embed.set_author(name=f"[{best.title}]({best.urls[0]})")
        embed.add_field(name="Similarity: ", value=f"{best.similarity}%")
        embed.add_field(name="Source: ", value=best.index)
        embed.set_image(url=best.thumbnail)
        embed.set_footer(text="<:mag_right:> This is what I have found!")
        await ctx.send(embed=embed)

    @_sauce.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await sauce_ctx()

    async def sauce_ctx(self, ctx):
        from pysaucenao import SauceNao, PixivSource, VideoSource, MangaSource
        sauce = SauceNao(api_key='18007b616a0808aa80ae9e17e3a8d110e53b081c')
        # results = await sauce.from_file('/path/to/image.png')
        results = await sauce.from_url(ctx.message.attachments[0].url)
        best = results[0]
        if isinstance(results[0], PixivSource):
            embed = discord.Embed(colour=discord.Colour.blurple(), title=best.author_name, url=best.author_url)
            embed.set_author(name=f"[{best.title}]({best.urls[0]})")
            embed.add_field(name="Similarity: ", value=f"{best.similarity}%")
            embed.add_field(name="Source: ", value=best.index)
            embed.set_image(url=best.thumbnail)
            embed.set_footer(text="<:mag_right:> This is what I have found!")
            await ctx.send(embed=embed)
        if isinstance(results[0], VideoSource):
            embed = discord.Embed(colour=discord.Colour.blurple(), title="")
            pass


    @commands.command(name="covid", description="Get COVID-19 infomation from a territory, region or country.")
    async def _covid(self, ctx, *, words:str):
        # Prints COVID-19 infomation in a country
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.covid19api.com/summary') as resp:
                covi = await resp.json()
        newConfirmed = 0
        totalConfirmed= 0
        newDeaths = 0
        totalDeaths= 0
        newRecovered = 0
        totalRecovered= 0
        try:
            print(covi['Countries'])
        except KeyError:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name="Service is temporarily unavailable at this time.")
            await ctx.send(embed=embed)
            return
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
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/239446877953720321/691020838379716698/unknown.png')
                await ctx.send(embed=embed)
                break

    @commands.command(hidden=True)
    async def countries(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Country names and country codes(ISO Alpha-2)")
        embed.add_field(name=".", value='var.countries')
        await ctx.send(embed=embed)

    @commands.command(name="math", description="Calculates.")
    # Test
    async def alpha(self, ctx, words:str):
        client = wolframalpha.Client('QPK7GG-8KK22QQTLJ')
        result = client.query(words)
        output = next(result.results).text
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=output)
        await ctx.send(embed=embed)

    @commands.command(name="server", description="Gets this server infomation.")
    async def _server(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple(), timestamp=ctx.message.created_at)
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed.add_field(name='Name:', value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name="Server ID:", value=ctx.guild.id, inline=True)
        embed.add_field(name='Owner:', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Verification Level:', value=ctx.guild.verification_level, inline=True)
        embed.add_field(name='Highest role:', value=ctx.guild.roles[-2], inline=True)
        embed.add_field(name="Region:", value=ctx.guild.region, inline=True)
        embed.add_field(name="Explicit Content Filter: ", value=ctx.guild.explicit_content_filter, inline=True)
        embed.add_field(name='Number Of Members', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Bots:', value=(', '.join(list_of_bots)))
        embed.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['gUser'], description="Get information of a GitHub user.")
    async def github_user(self, ctx, *, words):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.github.com/users/{words}') as resp:
                data = await resp.json()
        embed = discord.Embed(colour=discord.Colour.blurple(), title=data['login'], url=data['html_url'])
        embed.set_thumbnail(url=data['avatar_url'])
        embed.add_field(name="ID: ", value=data['id'])
        embed.add_field(name="Bio: ", value=data['bio'])
        embed.add_field(name="Public repos: ", value=data['public_repos'])
        embed.add_field(name="Public gists: ", value=data['public_gists'])
        embed.add_field(name="Followers: ", value=data['followers'])
        embed.add_field(name="Following: ", value=data['following'])
        embed.add_field(name="Website: ", value=data['blog'])
        embed.add_field(name="Email: ", value=data['email'])
        embed.add_field(name="Hireable: ", value=data['hireable'])
        embed.add_field(name="Joined at: ", value=data['created_at'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
