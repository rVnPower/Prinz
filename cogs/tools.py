#####################################################
import discord
from discord.ext import commands, tasks
#####################################################

class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()

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


def setup(bot):
    bot.add_cog(Tools(bot))