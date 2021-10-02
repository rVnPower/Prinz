from discord.ext import commands
import discord
import os
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer

from config import BOT_PREFIX, TEST_BOT_PREFIX
from utils.help import PrinzHelp
TEST_MODE = True

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=BOT_PREFIX if not TEST_MODE else TEST_BOT_PREFIX,
            case_insensitive=True,
            # case_insensitive_prefix=True,
            activity=discord.Activity(type=discord.ActivityType.competing, name='a boot up challenge'),
            owner_id=111111111,
            reconnect=True,
            max_messages=10000,
            chunk_guilds_at_startup=False,  # this is here for easy access. In case I need to switch it fast to False I won't need to look at docs.
            help_command=PrinzHelp(),
        )