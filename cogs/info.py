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
from pyowm.utils import config, timestamps
import requests
from chessdotcom import get_player_stats, get_leaderboards

import os
from pysaucenao import SauceNao, PixivSource, VideoSource, MangaSource, errors

from discord.ext.commands.cooldowns import BucketType
#####################################################
async def sauce_ctx(ctx, words):
    sauce = SauceNao(api_key='18007b616a0808aa80ae9e17e3a8d110e53b081c')

    # results = await sauce.from_file('/path/to/image.png')
    results = await sauce.from_url(words)
    for i in results:
        if isinstance(results[0], PixivSource):
            embed = discord.Embed(colour=discord.Colour.blurple(), title=i.author_name, url=i.author_url)
            try:
                embed.set_author(name=i.title, url=i.urls[0])
            except:
                embed.set_author(name=i.title)
            embed.add_field(name="Similarity: ", value=f"{i.similarity}%")
            embed.add_field(name="Source: ", value=i.index)
            embed.set_image(url=i.thumbnail)
            embed.set_footer(text=":mag_right: This is what I have found!")
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            try:
                embed.set_author(name=i.title, url=i.urls[0])
            except:
                embed.set_author(name=i.title)
            embed.add_field(name="Similarity: ", value=f"{i.similarity}%")
            embed.add_field(name="Source: ", value=i.index)
            embed.set_image(url=i.thumbnail)
            embed.set_footer(text=":mag_right: This is what I have found!")
            await ctx.send(embed=embed)
            return  

class Information(commands.Cog, description="Informative commands", name='Information'):
    def __init__(self, bot):
        self.bot = bot
        self.data = get_leaderboards().json

    @commands.command(aliases=['whois'], help='Check an user infomation.')
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(help="Check your Discord account details", aliases=['whoisme'])
    @commands.cooldown(1, 2, commands.BucketType.user)
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
        embed.add_field(name="Vanity URL: ", value=ctx.guild.vanity_url_code)
        await ctx.send(embed=embed)


    @commands.command(name="weather", help="Checks weather in a location.")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(name= "wikilan", help="Changes Wikipedia 's language.")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(name="wiki", help="Searches articles on Wikipedia")
    @commands.cooldown(1, 2, commands.BucketType.user)
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
                            try:
                                embed.set_image(url=wikipedia.summary(name, sentences=3).images[0])
                            except:
                                pass
                            await ctx.send(embed=embed)
                            return None
            except ValueError:
                if str(pinput.content).lower().strip() == 'cancel':
                    embed.set_author(name='Canceled!')
                    await ctx.send(embed=embed)
                    break
        await ctx.send(embed=embed)

    @commands.command(name="sauce", help="Find an image source.")
    @commands.cooldown(2, 600, commands.BucketType.user)
    async def sauce(self, ctx, *, url:str):
        await sauce_ctx(ctx, url)

    @sauce.error
    async def error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await sauce_ctx(ctx, ctx.message.attachments[0].url)
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(colour=discord.Colour.blurple(), title="Nothing found...")
            await ctx.send(embed=embed)

    @commands.command(name="covid", help="Get COVID-19 infomation from a territory, region or country.")
    @commands.cooldown(1, 2, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def countries(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Country names and country codes(ISO Alpha-2)")
        embed.add_field(name=".", value='var.countries')
        await ctx.send(embed=embed)

    @commands.command(help="Calculates.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    # Test
    async def alpha(self, ctx, *, words:str):
        client = wolframalpha.Client('QPK7GG-8KK22QQTLJ')
        result = client.query(words)
        output = next(result.results).text
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=output)
        await ctx.send(embed=embed)

    @commands.command(name="server", help="Gets this server infomation.")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(aliases=['gUser'], help="Get information of a GitHub user.")
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(help="Get information of a Osu! beatmap")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def osu_beatmap(self, ctx, *, words):
        API_URL = 'https://osu.ppy.sh/api/v2'
        TOKEN_URL = 'https://osu.ppy.sh/oauth/token'

        def get_token():
            data = {
                'client_id': 8954,
                'client_secret': 'EowlkKpcDXEGxagwbS7NF31ZQs6hl18ALPxcOUNX',
                'grant_type': 'client_credentials',
                'scope': 'public'
            }
            response = requests.post(TOKEN_URL, data=data)
            return response.json().get('access_token')

        def main():
            token = get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            params = {
                'id': words
            }
            response = requests.get(f'{API_URL}/beatmaps/lookup', params=params, headers=headers).json()
            return response
        data = main()
        try:
            embed = discord.Embed(colour=discord.Colour.blurple(), title=data['beatmapset']['title'], url=data['url'])
        except KeyError:
            embed = discord.Embed(colour=discord.Colour.blurple(), title="That beatmap does not exist!")
            await ctx.send(embed=embed)
        embed.set_author(name=data['beatmapset']['creator'])
        embed.add_field(name="Beatmap ID: ", value=data['beatmapset_id'])
        embed.add_field(name="Status: ", value=data['beatmapset']['status'])
        embed.add_field(name="Mode: ", value=data['mode'])
        embed.add_field(name="Difficulty rating: ", value=data['difficulty_rating'])
        embed.add_field(name="Last updated: ", value=data['beatmapset']['last_updated'])
        embed.add_field(name="Players: ", value=data['playcount'])
        embed.add_field(name="Passed players: ", value=data['passcount'])
        embed.add_field(name="Num. of circles: " , value=data['count_circles'])
        embed.add_field(name="Num. of sliders: ", value=data['count_sliders'])
        embed.add_field(name="Num. of spinners: ", value=data['count_spinners'])
        embed.add_field(name="Artist: ", value=data['beatmapset']['artist'])
        embed.set_image(url=data['beatmapset']['covers']['cover'])
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def osu_scores(self, ctx, *, words):
        API_URL = 'https://osu.ppy.sh/api/v2'
        TOKEN_URL = 'https://osu.ppy.sh/oauth/token'
        try:
            Type = words.split(' ')[1]
        except IndexError:
            Type = 'osu'

        def get_token():
            data = {
                'client_id': 8954,
                'client_secret': 'EowlkKpcDXEGxagwbS7NF31ZQs6hl18ALPxcOUNX',
                'grant_type': 'client_credentials',
                'scope': 'public'
            }
            response = requests.post(TOKEN_URL, data=data)
            return response.json().get('access_token')

        def main():
            token = get_token()
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            params = {
                'mode': Type
            }
            response = requests.get(f'{API_URL}/beatmaps/{words}/scores', params=params, headers=headers).json()
            return response
        data = main()
        print(data)

    @commands.command(help="Get information of a Geometry Dash level")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gd_level(self, ctx, ID:int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://gdbrowser.com/api/level/{ID}') as resp:
                r = await resp.json()
        if r != '-1':
            embed = discord.Embed(colour=discord.Colour.blurple())  
            embed.set_author(name=r['author'])
            embed.add_field(name=r['name'], value=
                f'''
                **Description**: {r["description"]}\n
                **ID**: {r["id"]}\n
                **Difficulty**: {r["difficulty"]}\n
                **Length**: {r["length"]}\n
                **Featured**: {r["featured"]}\n
                **Downloads**: {r["downloads"]}\n
                <:like:364076087648452610> **Likes:** {r["likes"]}\n
                **Required game version**: {r["gameVersion"]}\n
                **Song**: {r["songID"]} - {r["songName"]}
                ''', inline=True)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name="That level does not exist!")
        await ctx.send(embed=embed)

    @commands.command(help="Get information of a Geometry Dash player")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gd_player(self, ctx, *, words):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://gdbrowser.com/api/profile/{words}') as resp:
                r = await resp.json()
        embed = discord.Embed(colour=discord.Colour.blurple())
        if r != '-1':
            embed.set_author(name=r['username'])
            embed.add_field(name="Player ID: ", value=r['playerID'], inline=True)
            if int(r['rank']) == 0:
                embed.add_field(name="Rank: ", value="None", inline=True)
            else:
                embed.add_field(name="Rank: ", value=r['rank'], inline=True)
            embed.add_field(name="Stars: ", value=r['stars'], inline=True)
            embed.add_field(name="Diamonds: ", value=r['diamonds'], inline=True)
            embed.add_field(name="Secret coins: ", value=r['coins'], inline=True)
            embed.add_field(name="User coins:", value=r['userCoins'], inline=True)
            embed.add_field(name="Demons:", value=r['demons'], inline=True)
            embed.add_field(name="Creator points: ", value=r['cp'], inline=True)
        if r == '-1':
            embed.set_author(name="That player does not exist!")
        await ctx.send(embed=embed)

    @commands.command(help="Search something in Geometry Dash")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gd_search(self, ctx, *, words):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://gdbrowser.com/api/search/{words}?page=0') as resp:
                r = await resp.json()
        embed = discord.Embed(colour=discord.Colour.blurple())
        if r != '-1':
            for i in r:
                embed.set_author(name=f"Search results of {words} in Geometry Dash!")
                embed.add_field(name=f"{i['name']}", value=f"Likes: {i['likes']} | Downloads: {i['downloads']}", inline=False)
            await ctx.send(embed=embed)

    @commands.command(help="Get a category leaderboard on Chess.com")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def chess_top(self, ctx, *, words:str = "daily"):
        data2 = self.data['leaderboards']
        categories = self.data['leaderboards'].keys()
        for category in categories:
            if category == words.lower().strip():
                embed = discord.Embed(colour=discord.Colour.blurple(), title=f"Category: {category}")
                embed.set_author(name="Chess.com leaderboard!")
                for player in data2[category]:
                    embed.add_field(name=f"Rank: {player['rank']}", value=f"Username: {player['username']} | Rating: {player['score']}", inline=False)
                await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def chess_player(self, ctx, *, words:str = "VnPower"):
        def print_leaderboard(self, username):
            data = get_player_stats(username).json()
            categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
            embed = discord.Embed(colour=discord.Colour.blurple(), title=f"{words}'s stats on Chess.com")
            for category in categories:
                embed.add_field(name= f'Category: {category} |', value=f"Current: {data[category]['last']['rating']} | Best: {data[category]['best']['rating']}", inline=False)
            return embed
        embed = print_leaderboard(words)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
