# Standard Library
import asyncio
import itertools
import random
import discord
import contextlib

# Russian Roulette
from others.kill import outputs

# Red
from discord.ext import commands

class RussianRoulette(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.defaults = {
            "Cost": 50,
            "Chamber_Size": 6,
            "Wait_Time": 60,
            "Session": {"Pot": 0, "Players": [], "Active": False},
        }

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.guild_only()
    @commands.command()
    async def russian(self, ctx):
        """Start or join a game of russian roulette.

        The game will not start if no players have joined. That's just
        suicide.

        The maximum number of players in a circle is determined by the
        size of the chamber. For example, a chamber size of 6 means the
        maximum number of players will be 6.
        """
        settings = self.defaults
        if await self.game_checks(ctx, settings):
            await self.add_player(ctx, settings["Cost"])

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(hidden=True)
    async def rusreset(self, ctx):
        """ONLY USE THIS FOR DEBUGGING PURPOSES"""
        self.defaults.Session.clear()
        await ctx.send("The Russian Roulette session on this server has been cleared.")

    @commands.group(autohelp=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setrussian(self, ctx):
        """Russian Roulette Settings group."""
        pass

    @setrussian.command()
    async def chamber(self, ctx, size: int):
        """Sets the chamber size of the gun used. MAX: 12."""
        if not 1 < size <= 12:
            return await ctx.send("Invalid chamber size. Must be in the range of 2 - 12.")
        self.defaults.Chamber_Size.set(size)
        await ctx.send("Chamber size set to {}.".format(size))

    @setrussian.command()
    async def wait(self, ctx, seconds: int):
        """Set the wait time (seconds) before starting the game."""
        if seconds <= 0:
            return await ctx.send("You are an idiot.")
        self.defaults.Wait_Time.set(seconds)
        await ctx.send("The time before a roulette game starts is now {} seconds.".format(seconds))

    async def game_checks(self, ctx, settings):
        if settings["Session"]["Active"]:
            with contextlib.suppress(discord.Forbidden):
                await ctx.author.send("You cannot join or start a game of russian roulette while one is active.")
            return False

        if ctx.author.id in settings["Session"]["Players"]:
            await ctx.send("You are already in the roulette circle.")
            return False

        if len(settings["Session"]["Players"]) == settings["Chamber_Size"]:
            await ctx.send("The roulette circle is full. Wait for this game to finish to join.")
            return False

    async def add_player(self, ctx, cost):
        current_pot = self.defaults.Session.Pot()
        self.defaults.Session.Pot.set(value=(current_pot + cost))

        async with self.defaults.Session.Players() as players:
            players.append(ctx.author.id)
            num_players = len(players)

        if num_players == 1:
            wait = self.defaults.Wait_Time()
            await ctx.send(
                "{0.author.mention} is gathering players for a game of russian "
                "roulette!\nType `{0.prefix}russian` to enter. "
                "The round will start in {1} seconds.".format(ctx, wait)
            )
            await asyncio.sleep(wait)
            await self.start_game(ctx)
        else:
            await ctx.send("{} was added to the roulette circle.".format(ctx.author.mention))

    async def start_game(self, ctx):
        self.defaults.Session.Active.set(True)
        data = self.defaults.Session.all()
        players = [ctx.guild.get_member(player) for player in data["Players"]]
        filtered_players = [player for player in players if isinstance(player, discord.Member)]
        if len(filtered_players) < 2:
            await self.reset_game(ctx)
            return await ctx.send("You can't play by yourself. That's just suicide.\nGame reseted.")
        chamber = self.defaults.Chamber_Size()

        counter = 1
        while len(filtered_players) > 1:
            await ctx.send(
                "**Round {}**\n*{} spins the cylinder of the gun "
                "and with a flick of the wrist it locks into "
                "place.*".format(counter, ctx.bot.user.name)
            )
            await asyncio.sleep(3)
            await self.start_round(ctx, chamber, filtered_players)
            counter += 1
        await self.game_teardown(ctx, filtered_players)

    async def start_round(self, ctx, chamber, players):
        position = random.randint(1, chamber)
        while True:
            for turn, player in enumerate(itertools.cycle(players), 1):
                await ctx.send(
                    "{} presses the revolver to their head and slowly squeezes the trigger...".format(player.name)
                )
                await asyncio.sleep(5)
                if turn == position:
                    players.remove(player)
                    msg = "**BANG!** {0} is now dead.\n"
                    msg += random.choice(outputs)
                    await ctx.send(msg.format(player.mention, random.choice(players).name, ctx.guild.owner))
                    await asyncio.sleep(3)
                    break
                else:
                    await ctx.send("**CLICK!** {} passes the gun along.".format(player.name))
                    await asyncio.sleep(3)
            break

    async def game_teardown(self, ctx, players):
        winner = players[0]
        await ctx.send(
            "Congratulations {}! You are the last person standing and have ".format(winner.mention)
        )
        await self.reset_game(ctx)

    async def reset_game(self, ctx):
        self.defaults.Session.clear()

def setup(bot):
    bot.add_cog(RussianRoulette(bot))