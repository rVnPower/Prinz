import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import wikipedia
from saucenao_api import SauceNao
import requests
import json
import os
from os import listdir as o
from os.path import isfile, join
# from keep_alive import keep_alive

###########################################################
bot = commands.Bot(command_prefix='l!', help_command=None)
status = cycle(['League of Legends', 'osu!'])
TOKEN = 'ODY1NDg3NzQ2OTA1OTMxODQ2.YPEuRg.3_RCdpwXUFh0-DFsrvvwpiywDJA'
###########################################################

@tasks.loop(seconds=1200)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_ready():
    change_status.start()
    print("Logged in!")

@bot.event
async def on_message(message):
    send = [
        'Yes?', 'Do you need help? Type \'l!help\'!', 'I was playing...',
        'Don\'t you have something to do?', f'Hi! {message.author}!',
        'You mentioned me!'
    ]
    if bot.user.mentioned_in(message):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=random.choice(send))
        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You don\'t have permissions to do that!')
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You didn\'t pass in some arguments!')
        await ctx.send(embed=embed)
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You passed the wrong thing!')
        await ctx.send(embed=embed)
    else:
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# keep_alive()  # Starts a webserver to be pinged.
bot.run(TOKEN)