from discord_slash.utils.manage_commands import create_option
import discord
from discord.ext import commands, tasks
from discord_slash import cog_ext, SlashContext
from replit import db
##################################
guild_ids = []
guild_ids = db['guild']
alreadyIn = False
##################################
def update(result):
  if "guild" in db.keys():
    guild = db['guild']
    print(guild)
    for i in guild:
      if int(guild) == int(result):
        alreadyIn = True
        break
    else:
      guild.append(result)
      db['guild'] = guild
  else:
    db['guild'] = [result]


class Test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(name="verify", description="Add your server ID to bot's database!", guild_ids = guild_ids)
  async def verify(self, ctx):
    Gid = ctx.guild.id
    update(Gid)
    if alreadyIn == False:
      await ctx.send("Added successfully!")
    if alreadyIn == True:
      await ctx.send("You have already been verified!")

def setup(bot):
  bot.add_cog(Test(bot))