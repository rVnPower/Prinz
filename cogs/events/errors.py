import discord

from discord.ext import commands

from config import EMPTY_CHARACTER
from utils.embed import error_embed

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = error_embed("Error!", f'You do not have some permissions to use this! You are missing {", ".join(map(str, error.missing_perms))}. Contact server owner\'s if you think this was not supposed to happen.')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed = error_embed("Error!", f'You are missing some required parameters to use this! Use `l!help {ctx.message.content}` to find out what you are missing!')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.BadArgument):
            embed = error_embed("Error!", f"Looks like you are using this incorrectly. Use `l!help {ctx.message.content} to know how to use it! Maybe it just his spaghetti code...`")
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandNotFound):
            embed = error_embed("Error!", f'Well, there is no command named {ctx.message.content}. Use `l!help` to get a list of commands. Or if you want to... Then you can tell VnPower about your ideas! Maybe he will add it! If he can, ofc.')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed = error_embed("Error!", 'You are using this too fast! Wait {:.2f} seconds to use this again! Now you have some time to spare!'.format(error.retry_after))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NotOwner):
            embed = error_embed("Error!", 'Ok...I wi... Hold on! You are not VnPower. You are not my owner! You are not supposed to do this!! Get out!!!')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NSFWChannelRequired):
            embed = error_embed("Error!", 'What are you trying to do? Weird things? Then you should not be here. Go to a NSFW channel instead, you horny.')
            await ctx.send(embed=embed)
            return
        else:
            embed = error_embed("Error!", 'Uh oh... It does not work... We cannot do anything with this.')
            await ctx.send(embed=embed)
            raise error

def setup(bot):
    bot.add_cog(Errors(bot))