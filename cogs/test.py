from discord_slash.utils.manage_commands import create_option
import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
guild_ids = [865509913417482240]

class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(name="test",
             description="This is just a test command, nothing more.",
             options=[
               create_option(
                 name="optone",
                 description="This is the first option we have.",
                 option_type=3,
                 required=False
               )
             ])
  async def test(self, ctx, optone: str):
    await ctx.send(content=f"I got you, you said {optone}!")

def setup(bot):
  bot.add_cog(Test(bot))