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
###########################################################
bot = commands.Bot(command_prefix='l!', help_command=None)
lang= 'en'
bot.lang = lang
bot.lava_nodes = [
    {
        'host': 'lava.link',
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': 'whatever',
        'region': 'singapore'
    }
]
###########################################################

greetingsAndQuestion = json.loads(open('intents/greet.json', 'r').read())
trainList = []
for row in greetingsAndQuestion:
    trainList.append(row['question'])
    trainList.append(row['answer'])
chatbot = ChatBot('Prinz', logic_adapters=[
                        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I don\'t understand.',
            'maximum_similarity_threshold': 0.90
        }
        ])
trainer = ListTrainer(chatbot)
trainer.train(trainList)

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
    if message.guild is None:
        response = chatbot.get_response(message.content)
        try:
            await message.author.send(response)
        except discord.HTTPException:
            pass
    else:
        pass
    if bot.user.mentioned_in(message):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=random.choice(send))
        await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)

async def help2(ctx):
    count = 0
    commands = list(bot.cogs.values())
    
    embed = discord.Embed(colour=discord.Colour.blurple(), title="List of command types")
    embed.set_footer(text="Type 'l!help ' with a name of a type to see all of the commands!")
    for command in commands:
        if str(command.description) != '':
            embed.add_field(name=f"{command.qualified_name}", value=f"{command.description}", inline=False)
        else:
            embed.add_field(name=f"{command.qualified_name}", value=f"`No description provided`", inline=True)
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
        embed.add_field(name=command.name, value=f"`{command.description}`", inline=False)
    await ctx.send(embed=embed)

@bot.command(hidden=True)
async def test(ctx):
    await ctx.send(bot.lang)   

@h.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await help2(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'You don\'t have permissions to do that! You need {error.param.name}')
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
