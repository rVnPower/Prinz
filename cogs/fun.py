#####################################################
import discord
from discord.ext import commands, tasks
import time
import nekos
import asyncio
import aiohttp
import random
import json
from dadjokes import Dadjoke
from typing import Optional
import psutil

from discord.ext.commands.cooldowns import BucketType
from others.mem_profile import memory_usage_resource
from others.topics import topics
from config import MAIN_COLOR
from utils.embed import error_embed, normal_embed, success_embed
from utils.requests import get_requests_as_json
#####################################################
async def get_prefix(bot, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]
    except KeyError:
        prefixes[str(message.guild.id)] = 'l!'

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        return prefixes[str(message.guild.id)]

class Fun(commands.Cog, description="idk", name="Fun"):
    def __init__(self, bot):
        self.bot = bot
        self.t1 = time.time()

    @commands.command(name="hi", help="I will greet you!")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _hi(self, ctx):
        # Say hi!
        await ctx.send(f'Hi! {ctx.author.mention}')

    @commands.command(name="ping", help="Checks my latency.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _ping(self, ctx):
        # Checks bot latency
        t2 = time.time()
        n = t2-self.t1
        h = n // 3600
        s = n % 3600
        m = s // 60
        s = s % 60
        p = round(self.bot.latency * 1000)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.description = ("""**System CPU:**\n- Frequency: {0} Mhz\n- Cores: {1}\n- Usage: {2}%\n\n
                        **System Memory:**\n- Available: {3} MB\n- Total: {4} MB\n- Used: {5} MB\n\n
                        **System Disk:**\n- Total: {6} GB\n- Used: {7} GB\n- Free: {8} GB\n\n
                        **Process Info:**\n- Memory Usage: {9} MB\n- CPU Usage: {10}%\n- Threads: {11}""").format(round(psutil.cpu_freq().current, 2),
                                                                                                                psutil.cpu_count(), psutil.cpu_percent(),
                                                                                                                round(psutil.virtual_memory().available / 1048576),
                                                                                                                round(psutil.virtual_memory().total / 1048576),
                                                                                                                round(psutil.virtual_memory().used / 1048576),
                                                                                                                round(psutil.disk_usage("/").total / 1073741824, 2),
                                                                                                                round(psutil.disk_usage("/").used / 1073741824, 2),
                                                                                                                round(psutil.disk_usage("/").free / 1073741824, 2),
                                                                                                                round(self.bot.process.memory_full_info().rss / 1048576, 2),
                                                                                                                self.bot.process.cpu_percent(), self.bot.process.num_threads())
        embed.set_author(name=f'Pong! {p}ms!')
        embed.add_field(name="Runtime: ", value=f"{round(h)} hour{'s' if h > 1 else ''}, {round(m)} minute{'s' if round(m) > 1 else ''}, {round(s)} second{'s' if round(s) > 1 else ''}", inline=False)
        embed.add_field(name="Memory used: ", value=f"{memory_usage_resource()} MB", inline=True)
        await ctx.send(embed=embed)

    # @commands.command(help="Display informations about this bot.")
    # @commands.cooldown(1, 2, commands.BucketType.user)
    # async def info(self, ctx):
    #     # Prints infomation about the admin
    #     embed = discord.Embed(colour=discord.Colour.blurple(), description="Prinz is a simple Discord bot that was made for informations and anime. I do not want this bot to grow for now, because of Discord bad decisions.")
    #     embed.set_footer(text="Made from ❤️ | VnPower#8888", icon_url="https://cdn.discordapp.com/avatars/683670893515636749/7d8f6a81109fcc1c4afe451495b848e5.webp?size=1024")
    #     embed.add_field(name=f"{await get_prefix(self.bot, ctx)}help: ", value="For help", inline=True)
    #     embed.add_field(name=f"{await get_prefix(self.bot, ctx)}invite: ", value="DM you an invite link", inline=True)
    #     embed.add_field(name="Support us?", value="Vote for the bot: ")
    #     await ctx.send(embed=embed)

    @commands.command(help="Get a random textcat", aliases=['kao', 'kaoemoji'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def textcat(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.textcat)
        await ctx.send(r)

    @commands.command(help="Get a random fact")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def fact(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.fact)
        embed = discord.Embed(colour=discord.Colour.blurple(), title='Did you know?', description=r)
        await ctx.send(embed=embed)

    @commands.command(help="Get a random cat")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def cat(self, ctx):
        phrase = ['Meow!', 'Grrrr...', 'Nya~']
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.cat)
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url=r)
        embed.set_footer(text=random.choice(phrase))
        await ctx.send(embed=embed)

    @commands.command(help="Get a random `why?` question")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def why(self, ctx):
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.why)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=r.capitalize())
        await ctx.send(embed=embed)

    @commands.command(help="Answer your question with a random answer", aliases=['8ball'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def eightball(self, ctx, *, words:str):
        print(ctx.author)
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, nekos.eightball)
        if words.endswith('?'):
            embed = discord.Embed(colour=discord.Colour.blurple(), description=r.text.capitalize())
        else:
            embed = discord.Embed(colour=discord.Colour.blurple(), description="That does not look like a question.")
        await ctx.send(embed=embed)

    @commands.command(help="Get a random dog")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dog(self, ctx):
        embed = normal_embed("Woof!")
        embed.set_footer(text="Source: https://dog.ceo/api/breeds/image/random")
        result = get_requests_as_json(f'https://dog.ceo/api/breeds/image/random')
        embed.set_image(url=result['message'])
        await ctx.send(embed=embed)

    @commands.command(help="Get a random duck")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def duck(self, ctx):
        embed = normal_embed("Quack!")
        embed.set_footer(text="Source: https://random-d.uk/api/random?format=json")
        result = get_requests_as_json(f'https://random-d.uk/api/random?format=json')
        embed.set_image(url=result['url'])
        await ctx.send(embed=embed)

    @commands.command(help="Emojify a string")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def emojify(self, ctx, *, words:str):
        emojis = []
        for s in words.lower():
            if s.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two',
                            '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(''.join(emojis))

    @commands.command(help="Tell you a joke", aliases=['joke', 'jk'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def tellmeajoke(self, ctx):
        embed = discord.Embed(color=discord.Color.blurple())
        result = await get_requests_as_json(f'https://yourmommmaosamaobama.hisroyal123.repl.co/?message=tell%me%a%joke')
        embed.description = result['message']
        await ctx.send(embed=embed)

    @commands.command(help="Flip a coin... or a user. (Thanks to RedBot)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def flip(self, ctx, user: discord.Member = None):
        """Flip a coin... or a user.
        Defaults to a coin.
        """
        if user is not None:
            msg = ""
            if user.id == ctx.bot.user.id:
                user = ctx.author
                msg = "Nice try. You think this is funny?\n How about *this* instead:\n\n"
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = user.display_name.translate(table)
            char = char.upper()
            tran = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
            table = str.maketrans(char, tran)
            name = name.translate(table)
            await ctx.send(msg + "(╯°□°）╯︵ " + name[::-1])
        else:
            await ctx.send("*flips a coin and... ") + random.choice(["HEADS!*", "TAILS!*"])

    @commands.command(help="Sends a random topic")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def topic(self, ctx):
        await ctx.send(random.choice(topics))

    @commands.command(aliases=['fm', 'firstmsg', 'firstmessage', 'first_msg'], help="Get the first message of the channel.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.bot_has_permissions(read_message_history=True)
    async def first_message(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        channel = channel or ctx.channel
        async for message in channel.history(limit=1, oldest_first=True):
            return await ctx.reply(embed=discord.Embed(
                title=f"First message in `{channel.name}`",
                url=message.jump_url,
                color=MAIN_COLOR
            ))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Convert your text into a mock")
    async def mock(self, ctx, *, text=None):

        PREFIX = ctx.clean_prefix

        if text is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Incorrect Usage!", f"Please enter some text next time!\nCorrect Usage: `{PREFIX}mock <text>`"))

        res = ""
        i = 0
        for c in text:
            if i % 2 == 0:
                res += c.lower()
            else:
                res += c.upper()
            i += 1
        await ctx.reply(res)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["atc"], help="Makes your text look beautiful")
    async def aesthetic(self, ctx, *, args=None):
        PREFIX = ctx.clean_prefix
        if args is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Invalid args", f"Correct usage: `{PREFIX}atc <msg> | [mode]`.\nMode can be `b` (bold), `i` (italic), or `n` (none).\n\nExample: `{PREFIX}atc uwu | n`\nOutput: `u w u`"))

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        s += "**" if m == "b" else ("_" if m == "i" else "")

        msg = args.split(" | ")[0]
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        s += "**" if m == "b" else ("_" if m == "i" else "")

        await ctx.reply(s)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Funny, funny jokes!")
    async def dadjoke(self, ctx):
        dadjoke = Dadjoke()
        await ctx.reply(embed=success_embed("Haha!", dadjoke.joke))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Funny, funny memes!")
    async def meme(self, ctx: commands.Context):
        
        data = await get_requests_as_json("https://meme-api.herokuapp.com/gimme")
        return await ctx.reply(embed=success_embed(
            "Haha!",
            data['title']
        ).set_image(url=data['url']))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get a random quote!")
    async def quote(self, ctx):
        results = await get_requests_as_json('https://type.fit/api/quotes')
        result = random.choice(results)
        await ctx.message.reply(embed=success_embed("Quote!", f"{result['text']} ~ {result['author']}"))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get a random advice!")
    async def advice(self, ctx):
        result = await get_requests_as_json('https://api.adviceslip.com/advice')
        await ctx.message.reply(embed=success_embed("Advice!", result['slip']['advice']))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Gives you a random name.")
    async def randomname(self, ctx):
        result = await get_requests_as_json('https://nekos.life/api/v2/name')
        await ctx.message.reply(embed=success_embed("Random Name!", result['name']))

def setup(bot):
    bot.add_cog(Fun(bot))
