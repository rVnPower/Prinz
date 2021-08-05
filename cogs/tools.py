#####################################################
import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
#####################################################

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def binary(self, ctx, *, words):
        Type = words.split(' ')[0]
        string = words.split(str(Type+' '))
        if Type.lower().strip() == 'decode':
            string = string[1]
            binary_values = string.split()
            ascii_string = ""
            for binary_value in binary_values:
                an_integer = int(binary_value, 2)
                ascii_character = chr(an_integer)
                ascii_string += ascii_character
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name=f'Output: {ascii_string}')
            await ctx.send(embed=embed)
        if Type.lower().strip() == 'encode':
            string = string[1]
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name="Output: "+" ".join(f"{ord(i):08b}" for i in string))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name=f'Please provide a type! (Ex: "decode" or "encode")')
            await ctx.send(embed=embed)

    @commands.command()
    async def add(self, ctx):
        Gid = ctx.guild.id
        with open("id.txt", "r") as file_object:
            for i in range(1, 1000):
                check = file_object.readlines(i)
                if int(check) == int(Gid):
                    await ctx.send('bruh')
'''
        with open("id.txt", "a") as file_object:
            for i in len(file_object):
            for i in lis:
                file_object.write(i + '\n')'''


def setup(bot):
    bot.add_cog(Tools(bot))