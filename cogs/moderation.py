#####################################################
import discord
from discord.ext import commands, tasks
import random
from discord_slash import cog_ext, SlashContext
from replit import db
guild_ids = []
guild_ids = db['guild']
#####################################################

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(colour=discord.Colour.blurple())
        try:
            await member.kick(reason=reason)
            embed.add_field(name=f'Kicked {member}!',
                            value=f'Reason: {reason}',
                            inline=False)
        except Exception:
            embed.add_field(name=f'Something went wrong...',
                            value='Did you give the permission to the bot?',
                            inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(colour=discord.Colour.blurple())
        try:
            await member.ban(reason=reason)
            embed.add_field(name=f'Banned {member}!',
                            value=f'Reason: {reason}',
                            inline=False)
        except Exception:
            embed.add_field(name=f'Something went wrong...',
                            value='Did you give the permission to the bot?',
                            inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

def setup(bot):
    bot.add_cog(Moderation(bot))