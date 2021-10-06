#####################################################
import discord
from discord.utils import escape_markdown
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
import datetime
import time
import codecs
import pathlib

import os
from pysaucenao import SauceNao, PixivSource, VideoSource, MangaSource, errors
from typing import List, Optional, Union

from discord.ext.commands.cooldowns import BucketType

from utils.embed import error_embed
from utils.time import datetime_to_seconds
from config import ORANGE_COLOR, MAIN_COLOR, EMOJIS
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

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Get COVID-19 stats about any country.")
    async def covid(self, ctx, *, country=None):
        PREFIX = ctx.clean_prefix
        if country is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Invalid Usage!", f"Please use it like this: `{PREFIX}covid <country>`"))

        try:
            async with self.bot.session.get(f"https://coronavirus-19-api.herokuapp.com/countries/{country.lower()}") as r:
                response = await r.json()
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Error!", f"Couldn't find COVID-19 stats about `{country}`."))

        country = response['country']
        total_cases = response['cases']
        today_cases = response['todayCases']
        total_deaths = response['deaths']
        today_deaths = response['todayDeaths']
        recovered = response['recovered']
        active_cases = response['active']
        critical_cases = response['critical']
        total_tests = response['totalTests']
        cases_per_one_million = response['casesPerOneMillion']
        deaths_per_one_million = response['deathsPerOneMillion']
        tests_per_one_million = response['testsPerOneMillion']

        embed = discord.Embed(
            title=f"COVID-19 Status of {country}",
            description="This information isn't always live, so it may not be accurate.",
            color=ORANGE_COLOR
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")

        embed.add_field(
            name="Total",
            value=f"""
```yaml
Total Cases: {total_cases}
Total Deaths: {total_deaths}
Total Tests: {total_tests}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Today",
            value=f"""
```yaml
Today Cases: {today_cases}
Today Deaths: {today_deaths}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Other",
            value=f"""
```yaml
Recovered: {recovered}
Active Cases: {active_cases}
Critical Cases: {critical_cases}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Per One Million",
            value=f"""
```yaml
Cases Per One Million: {cases_per_one_million}
Deaths Per One Million: {deaths_per_one_million}
Tests Per One Million: {tests_per_one_million}
```
            """,
            inline=False
        )

        await ctx.message.reply(embed=embed)

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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(help="Get info about a role.")
    async def roleinfo(self, ctx: commands.Context, role: discord.Role = None):
        prefix = ctx.clean_prefix
        if role is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a role to get info about.\nCorrect Usage: `{prefix}roleinfo @role`"
            ))
        embed = discord.Embed(
            title=f"{EMOJIS['tick_yes']} Role Information",
            color=role.color
        )
        embed.add_field(
            name="Basic Info:",
            value=f"""
```yaml
Name: {role.name}
ID: {role.id}
Position: {role.position}
Color: {str(role.color)[1:]}
Hoisted: {role.hoist}
Members: {len(role.members)}
```
            """,
            inline=False
        )
        something = ""
        for permission in role.permissions:
            a, b = permission
            a = ' '.join(a.split('_')).title()
            hmm = '+' if b else '-'
            something += hmm + ' ' + a + '\n'
        embed.add_field(
            name="Permissions:",
            value=f"```diff\n{something}\n```",
            inline=False
        )
        await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get info about users!")
    async def userinfo(self, ctx, user: Optional[Union[discord.Member, discord.User]] = None):
        if isinstance(ctx, commands.Context):
            user = user or ctx.author
        else:
            user = user or ctx.target

        _user = await self.bot.fetch_user(user.id)  # to get the banner

        embed = discord.Embed(
            color=_user.accent_color or user.color or MAIN_COLOR,
            description=f"{user.mention} {escape_markdown(str(user))} ({user.id})",
            timestamp=datetime.datetime.utcnow()
        ).set_author(name=user, icon_url=user.display_avatar.url
        ).set_footer(text=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        ).set_thumbnail(url=user.display_avatar.url
        )
        if _user.banner is not None:
            embed.set_image(url=_user.banner.url)

        embed1 = embed.copy()
        c = str(int(user.created_at.astimezone(datetime.timezone.utc).timestamp()))
        j = str(int(user.joined_at.astimezone(datetime.timezone.utc).timestamp())) if isinstance(user, discord.Member) else None
        embed1.add_field(
            name="Account Info:",
            value=f"""
**Username:** {escape_markdown(user.name)}
**Nickname:** {escape_markdown(user.display_name)}
**ID:** {user.id}
            """,
            inline=False
        )
        embed1.add_field(
            name="Age Info:",
            value=f"""
**Created At:** <t:{c}:F> <t:{c}:R>
**Joined At:** {'<t:' + j + ':F> <t:' + j + ':R>' if j is not None else 'Not in the server.'}
            """,
            inline=False
        )
        embed1.add_field(
            name="URLs:",
            value=f"""
**Avatar URL:** [Click Me]({user.display_avatar.url})
**Guild Avatar URL:** [Click Me]({(user.guild_avatar.url if user.guild_avatar is not None else user.display_avatar.url) if isinstance(user, discord.Member) else user.display_avatar.url})
**Banner URL:** {'[Click Me](' + _user.banner.url + ')' if _user.banner is not None else 'None'}
            """,
            inline=False
        )

        embed2 = embed.copy()
        r = (', '.join(role.mention for role in user.roles[1:][::-1]) if len(user.roles) > 1 else 'No Roles.') if isinstance(user, discord.Member) else 'Not in server.'
        embed2.add_field(
            name="Roles:",
            value=r if len(r) <= 1024 else r[0:1006] + ' and more...',
            inline=False
        )

        embed3 = embed.copy()
        embed3.add_field(
            name="Permissions:",
            value=', '.join([perm.replace('_', ' ').title() for perm, value in iter(user.guild_permissions) if value]) if isinstance(user, discord.Member) else 'Not in server.',
            inline=False
        )
        embeds = [embed1, embed2, embed3]
        await ctx.reply(embed=embed1)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get info about the server!")
    async def serverinfo(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Information",
            description=f"Description: {guild.description}",
            color=MAIN_COLOR
        ).set_author(
            name=guild.name,
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        ).set_footer(text=f"ID: {guild.id}")
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(
            name="Basic Info:",
            value=f"""
**Owner:** <@{guild.owner_id}>
**Created At:** <t:{round(time.time() - (datetime_to_seconds(guild.created_at) - time.time()))}:F>
**Region:** {str(guild.region).title()}
**System Channel:** {"None" if guild.system_channel is None else guild.system_channel.mention}
**Verification Level:** {str(guild.verification_level).title()}
            """,
            inline=False
        )
        embed.add_field(
            name="Members Info:",
            value=f"""
**Members:** `{len(guild.members)}`
**Humans:** `{len(list(filter(lambda m: not m.bot, guild.members)))}`
**Bots:** `{len(list(filter(lambda m: m.bot, guild.members)))}`
            """,
            inline=True
        )
        embed.add_field(
            name="Channels Info:",
            value=f"""
**Categories:** `{len(guild.categories)}`
**Text Channels:** `{len(guild.text_channels)}`
**Voice Channels:** `{len(guild.voice_channels)}`
**Threads:** `{len(guild.threads)}`
            """,
            inline=True
        )
        embed.add_field(
            name="Other Info:",
            value=f"""
**Roles:** `{len(guild.roles)}`
**Emojis:** `{len(guild.emojis)}`
**Stickers:** `{len(guild.stickers)}`
                """
        )
        if guild.features:
            embed.add_field(
                name="Features:",
                value=', '.join([feature.replace('_', ' ').title() for feature in guild.features]),
                inline=False
            )
        if guild.banner is not None:
            embed.set_image(url=guild.banner.url)

        return await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['av', 'pfp'], help="Get the user's avatar")
    async def avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None):
        user = user or ctx.author
        embed = discord.Embed(
            title=f"Avatar of {escape_markdown(str(user))}",
            color=user.color,
            description=f'Link as: [`png`]({user.display_avatar.replace(format="png").url}) | [`jpg`]({user.display_avatar.replace(format="jpg").url}) | [`webp`]({user.display_avatar.replace(format="webp").url})'
        ).set_image(url=user.display_avatar.url)
        await ctx.message.reply(embed=embed)

    @commands.command(aliases=['lc'],
                      help="Lines of python code used making the bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def linecount(self, ctx):
        """ Lines of python code used making the bot """

        pylines = 0
        pyfiles = 0
        for path, subdirs, files in os.walk('.'):
            for name in files:
                if name.endswith('.py'):
                    pyfiles += 1
                    with codecs.open('./' + str(pathlib.PurePath(path, name)), 'r', 'utf-8') as f:
                        for i, l in enumerate(f):
                            if l.strip().startswith('#') or len(l.strip()) == 0:  # skip commented lines.
                                pass
                            else:
                                pylines += 1

        await ctx.send("I am made up of **{0}** files and **{1}** lines of code.\n".format(f'{pyfiles:,}', f'{pylines:,}'))

def setup(bot):
    bot.add_cog(Information(bot))
