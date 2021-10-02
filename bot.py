import discord
from discord.ext import commands, tasks

import aiohttp
import os
import asyncio
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
from utils.help import PrinzHelp
from config import BOT_TOKEN, TEST_TOKEN, BOT_PREFIX, TEST_BOT_PREFIX, EXTENSIONS
from utils.bot import Bot

TEST_MODE = True

bot = commands.Bot(command_prefix=BOT_PREFIX if not TEST_MODE else TEST_BOT_PREFIX,
            case_insensitive=True,
            # case_insensitive_prefix=True,
            activity=discord.Activity(type=discord.ActivityType.competing, name='a boot up challenge'),
            owner_id=881015410110124032,
            reconnect=True,
            max_messages=10000,
            chunk_guilds_at_startup=False,  # this is here for easy access. In case I need to switch it fast to False I won't need to look at docs.
            help_command=PrinzHelp())

for cog in EXTENSIONS:
    bot.load_extension(cog)

bot.run(BOT_TOKEN if not TEST_MODE else TEST_TOKEN)
