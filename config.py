from dotenv import load_dotenv
import os

# A file that contains tokens and related stuff

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
TEST_TOKEN = os.getenv("TEST_TOKEN") # Test bot token

# APIs token
OSU_TOKEN = os.getenv("OSU_TOKEN")
PYSAUCENAO_TOKEN = os.getenv("PYSAUCENAO_TOKEN")
OWM_TOKEN = os.getenv("OWM_TOKEN")

# Bot's variable
EMPTY_CHARACTER = "‎"
BOT_PREFIX = "l!"
TEST_BOT_PREFIX = "t!"

# Colors
MAIN_COLOR = 0x0080FF  # light blue kinda
RED_COLOR = 0xFF0000
ORANGE_COLOR = 0xFFA500
YELLOW_COLOR = 0xFFC300
PINK_COLOR = 0xe0b3c7
PINK_COLOR_2 = 0xFFC0CB
STARBOARD_COLOR = 15655584

# LINK
EMOJIS = {
    "tick_no": "❌",
    "tick_yes": "✔️",
    "loading": "<a:typing:883912551367327824>",
    'nsfw': '🔞',
    'flushed': "<:HyperFlushed:661729636513742853>",
    'heart': "<:heart_boost:878671895690633247>",
}

# COGS
EXTENSIONS = [
    'cogs.anime',
    'cogs.emojis',
    'cogs.fun',
    'cogs.game',
    'cogs.info',
    'cogs.mod',
    'cogs.music',
    # 'cogs.musictest2',
    'cogs.NSFW',
    'cogs.owner',
    'cogs.utility',
    'cogs.images',
    'cogs.events.errors',
    'cogs.events.events',
]