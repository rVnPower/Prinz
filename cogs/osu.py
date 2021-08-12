#####################################################
import discord
from discord.ext import commands, tasks
import random
import requests
import json
#####################################################

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

    @commands.command()
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

def setup(bot):
	bot.add_cog(Osu(bot))