import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from dotenv import load_dotenv
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from keep_alive import keep_alive
greetingsAndQuestion = json.loads(open('greet.json', 'r').read())

trainList = []

for row in greetingsAndQuestion:
    trainList.append(row['question'])
    trainList.append(row['answer'])

chatbot = ChatBot('Prinz')

trainer = ListTrainer(chatbot)

trainer.train(trainList)
###########################################################
bot = commands.Bot(command_prefix='l!', help_command=None)
###########################################################

@tasks.loop(seconds=600)
async def change_status():
    status = cycle([f'l!invite = {str(len(bot.guilds))} servers += 1!'])
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
async def on_ready():
    change_status.start()
    print("Logged in!")

@bot.event
async def on_message(message):
    send = [
        'Yes?', 'Do you need help? Type \'l!help\'!', 'I was playing...',
        'Don\'t you have something to do?',
        'You mentioned me!'
    ]

    if bot.user.mentioned_in(message):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=random.choice(send))
        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)

async def help2(ctx):
    count = 0
    commands = ['Anime', 'Chess', 'Doujin', 'Games', 'GD (Geometry Dash)', 'Information', 'Math', 'Moderation', 'Music', 'Osu', 'Simple', 'Tools']
    embed = discord.Embed(colour=discord.Colour.blurple(), title="List of command types")
    embed.set_footer(text="Type 'l!help ' with a name of a type to see all of the commands!")
    for i in commands:
        count += 1
        embed.add_field(name=f"{count}. ", value=i, inline=True)
    await ctx.send(embed=embed)

@bot.command(aliases=['help'])
async def h(ctx, *, words:str):
    r1 = bot.get_cog(words.capitalize())
    try:
        commands = r1.get_commands()
    except AttributeError:
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="That type does not exist!")
        await ctx.send(embed=embed)
        return
    commands = r1.get_commands()

    embed = discord.Embed(colour=discord.Colour.blurple(), title=f"Commands in {words.capitalize()}")
    for command in commands:
        embed.add_field(name=command.name, value=f"`{command.description}`")
    await ctx.send(embed=embed)
    

@h.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await help2(ctx)

@bot.command(name="Hi!", description="This is just a test command, nothing more.")
async def load(ctx, extension):
    if str(ctx.author) == 'VnPower#8888':
        bot.load_extension(f'cogs.{extension}')
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Loaded {extension} successfully!')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You don\'t have permissions to do that! This is a special command!')
        await ctx.send(embed=embed)

@bot.command()
async def unload(ctx, extension):
    if str(ctx.author) == 'VnPower#8888':
        bot.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Unloaded {extension} successfully!')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You don\'t have permissions to do that! This is a special command!')
        await ctx.send(embed=embed)

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
        embed.set_author(name='You passed the wrong value!')
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='That command does not exist!')
        await ctx.send(embed=embed)
    else:
        raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
load_dotenv()
bot.run(os.getenv("TOKEN"))
