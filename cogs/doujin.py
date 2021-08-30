#####################################################
import discord
from discord.ext import commands, tasks
import asyncio
from NHentai.nhentai import NHentai
#####################################################

class Doujin(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rD'], description="Get a random doujin on NHentai")
    async def random_doujin(self ,ctx):
        if ctx.channel.is_nsfw():
            nhentai = NHentai()
            Doujin = nhentai.get_random()
            embed = discord.Embed(colour=discord.Colour.blurple(), title=Doujin.title, url=f'https://nhentai.net/g/{Doujin.id}')
            embed.set_image(url=Doujin.images[0])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name='You can only use this command in a NSFW channel!')
            await ctx.send(embed=embed)

    @commands.command(description="Read a doujin on NHentai")
    async def read_doujin(self, ctx, *, words:int):
        current = 0
        nhentai = NHentai()
        Doujin = nhentai.get_doujin(id=words)
        embeds = []
        # Start looping
        for i in Doujin.images:
            current +=1
            embed = discord.Embed(colour=discord.Colour.blurple())
            embed.set_author(name=f"Page {current}/{len(Doujin.images)-1}")
            embed.set_image(url=i)
            embeds.append(embed)
        current = 0
        # Add reactions and do stuff
        buttons = ['⏪', '◀️', '▶️', '⏩']
        msg = await ctx.send(embed=embeds[current])
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji in buttons, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Time out!")
                return
            else:
                previous_page = current
                if reaction.emoji == '⏪':
                    current = 0
                elif reaction.emoji == '◀️':
                    if current > 0:
                        current -= 1
                    else:
                        current = len(embeds) - 1
                elif reaction.emoji == '▶️':
                    if current < len(embeds):
                        current += 1
                    else:
                        current = 0
                elif reaction.emoji == '⏩':
                    current = len(embeds) - 1
                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)
                    if current != previous_page:
                        await msg.edit(embed=embeds[current])

def setup(bot):
    bot.add_cog(Doujin(bot))