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
            embed = error_embed("Error!", f'Wowza. You are missing {", ".join(map(str, error.missing_perms))}to run this command.')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed = error_embed("Error!", 'You are missing something for the commands to work. Use \'help \'command to learn more about this command.')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.BadArgument):
            embed = error_embed("Error!", "I didn't ask you to pass in those arguments. Use \'help \'command to learn more about this command.")
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandNotFound):
            embed = error_embed("Error!", 'No commands found. But the \'help\' command is here for you.')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed = error_embed("Error!", 'Wowza. You are going too fast! Try again after {:.2f}s'.format(error.retry_after))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NotOwner):
            embed = error_embed("Error!", 'You are not my owner!')
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NSFWChannelRequired):
            embed = error_embed("Error!", 'This is a NSFW command. You know what it means.')
            await ctx.send(embed=embed)
            return
        else:
            embed = error_embed("Error!", 'The command failed to execute. Please report this if you can.')
            await ctx.send(embed=embed)
            raise error

def setup(bot):
    bot.add_cog(Errors(bot))