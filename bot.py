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
import aiohttp

def get_prefix(bot, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        prefixes[str(message.guild.id)] = 'l!'

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        return prefixes[str(message.guild.id)]


###########################################################
bot = commands.Bot(command_prefix= get_prefix)
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
async def on_guild_join(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'l!'

    with open('data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_leave(guild):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open('data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'You don\'t have permissions to do that! You need `{", ".join(map(str, error.missing_perms))}`!')
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You didn\'t pass in some arguments!')
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='You passed the wrong value!')
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='That command does not exist!')
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='This command is on cooldown! Please try again after {:.2f}s'.format(error.retry_after))
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name='An error occurred while executing this command.')
        await ctx.send(embed=embed)
        raise error


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive()
load_dotenv()
# bot.run(os.getenv("TOKEN"))
bot.run("ODg2NDQxMTAyNDEwOTE1ODQw.YT1onA.T2vi9V-YigHzRUlqAmQlw-fi__c")
