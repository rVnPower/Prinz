import discord

from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        m = "Logged in as:"
        m += "\nName: {0} ({0.id})".format(self.bot.user)
        print(m)
        await self.bot.change_presence(status='online', activity=discord.Activity(type=discord.ActivityType.playing, name="nothing"))

def setup(bot):
    bot.add_cog(Events(bot))