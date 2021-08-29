#####################################################
import discord
from discord.ext import commands, tasks
import math
import random
#####################################################

class Math(commands.Cog, description="Math commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="binary", description="Convert everything to binary.")
    async def _binary(self, ctx, *, words:str):
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
        elif Type.lower().strip() == 'encode':
            string = string[1]
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name="Output: "+" ".join(f"{ord(i):08b}" for i in string))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name=f'Please provide a type! (Ex: "decode" or "encode")')
            await ctx.send(embed=embed)

    @commands.command(description="Check if an integer is a prime number")
    async def prime(self, ctx, n:int):
        m = math.sqrt(abs(n))
        i = 2
        while n % i != 0 and i <=n:
            i += 1
            if i>m and n>=2:
                await ctx.send(f'{n} is a prime number!')
                break
        else:
            await ctx.send(f'{n} is not a prime number!')

def setup(bot):
    bot.add_cog(Math(bot))