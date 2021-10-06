import discord
import aiohttp
from discord.ext import commands
from cogs import musictest2

from datetime import datetime, timezone, timedelta

class not_voted(commands.CheckFailure):
    pass

class admin_only(commands.CheckFailure):
    pass

class music_error(commands.CheckFailure):
    pass

def add_vote(bot, user, time=datetime.utcnow(), voted=True):
    bot.voted[user] = {"voted": voted, "expire": time + timedelta(hours=12) if voted else time + timedelta(seconds=10)}

def has_voted():
    async def predicate(ctx):
        if await ctx.bot.is_booster(ctx.author):
            return True
        elif ctx.guild.id == 709521003759403063:
            return True
        else:
            get_vote = ctx.bot.cache.get(ctx.bot, "voted", ctx.author.id)
            if get_vote:
                time = (get_vote["expire"] - datetime.utcnow()).total_seconds()
                if get_vote["voted"] and time > 0:
                    return True
                elif get_vote["voted"] and time <= 0:
                    ctx.bot.voted.pop(ctx.author.id)
                    pass
                elif not get_vote["voted"] and time > 0:
                    raise not_voted()
                elif not get_vote["voted"] and time <= 0:
                    ctx.bot.voted.pop(ctx.author.id)
                    pass
            try:
                try:
                    if await ctx.bot.dblpy.get_user_vote(ctx.author.id):
                        add_vote(ctx.bot, ctx.author.id, True)
                        return True
                except Exception:
                    pass
                async with aiohttp.ClientSession() as session:
                    auth = {'Authorization': ctx.bot.config.STAT_TOKEN}
                    async with session.get(f'https://api.statcord.com/v3/667117267405766696/votes/{ctx.author.id}?days=0.5', headers=auth) as r:
                        js = await r.json()
                        color = ctx.bot.settings['colors']
                        e = discord.Embed(color=color['deny_color'], title='Something failed')
                        e.set_author(name=f"Hey {ctx.author}!", icon_url=ctx.author.avatar_url)
                        if js['error'] is False and js['didVote'] is False:
                            add_vote(ctx.bot, ctx.author.id, voted=False)
                            raise not_voted()
                        elif js['error'] is False and js['didVote'] is True:
                            add_vote(ctx.bot, ctx.author.id, time=datetime.utcfromtimestamp(js['data'][0]['timestamp']))
                            return True
                        elif js['error'] is True:
                            ctx.bot.dispatch('silent_error', ctx, js['message'], trace_error=False)
                            e.description = "Oops!\nError occured while fetching your vote: {0}".format(js['message'])
                            await ctx.send(embed=e)
                            return False
            except not_voted:
                raise not_voted()
            except Exception as e:
                ctx.bot.dispatch('silent_error', ctx, e)
                raise commands.BadArgument("Error occured when trying to fetch your vote, sent the detailed error to my developers.\n```py\n{0}```").format(e)
    return commands.check(predicate)

def is_admin():
    async def predicate(ctx):
        if await ctx.bot.is_admin(ctx.author):
            return True
        raise admin_only()
    return commands.check(predicate)

def test_command():  # update this embed
    async def predicate(ctx):
        cache = ctx.bot.cache.get(ctx.bot, 'testers', ctx.guild.id)
        if await ctx.bot.is_admin(ctx.author):
            return True
        elif not await ctx.bot.is_admin(ctx.author) and not cache:
            await ctx.send("This command is in its testing phase, you can join the support server "
                             "if you want to apply your guild to be a testing guild or know when the command "
                             "will be available.")
            return False
        elif not await ctx.bot.is_admin(ctx.author) and cache:
            return True
        return False
    return commands.check(predicate)

def check_music(author_channel=False, bot_channel=False, same_channel=False, verify_permissions=False, is_playing=False, is_paused=False):
    async def predicate(ctx):
        player = ctx.bot.wavelink.get_player(ctx.guild.id, cls=musictest2.Player, context=ctx)
        author_voice = getattr(ctx.author.voice, 'channel', None)
        bot_voice = getattr(ctx.guild.me.voice, 'channel', None)
        if author_channel and not getattr(ctx.author.voice, 'channel', None):
            raise music_error("{0} You need to be in a voice channel first.").format(ctx.bot.settings['emojis']['misc']['warn'])
        if bot_channel and not getattr(ctx.guild.me.voice, 'channel', None):
            raise music_error("{0} I'm not in the voice channel.").format(ctx.bot.settings['emojis']['misc']['warn'])
        if same_channel and bot_voice and author_voice != bot_voice:
            raise music_error("{0} You need to be in the same voice channel with me.").format(ctx.bot.settings['emojis']['misc']['warn'])
        if verify_permissions and not ctx.author.voice.channel.permissions_for(ctx.guild.me).speak or not ctx.author.voice.channel.permissions_for(ctx.guild.me).connect:
            raise music_error("{0} I'm missing permissions in your voice channel. Make sure you have given me the correct permissions!").format(ctx.bot.settings['emojis']['misc']['warn'])
        if is_playing and not player.is_playing:
            raise music_error("{0} I'm not playing anything.").format(ctx.bot.settings['emojis']['misc']['warn'])
        if is_paused and not player.is_paused and ctx.command.name == 'resume':
            raise music_error("{0} Player is not paused.").format(ctx.bot.settings['emojis']['misc']['warn'])
        if is_paused and player.is_paused and ctx.command.name == 'pause':
            raise music_error("{0} Player is already paused.").format(ctx.bot.settings['emojis']['misc']['warn'])
        dj_voice = getattr(player.dj.voice, 'channel', None)
        return True
    return commands.check(predicate)