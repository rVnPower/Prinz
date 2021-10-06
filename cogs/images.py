import functools
import discord

from discord.ext import commands
from typing import Optional
from epicbot_images import effects

from config import EMOJIS

class Images(commands.Cog, description="Things with images", name="Images"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Blur your friends ugly face...")
    @commands.bot_has_permissions(attach_files=True)
    @commands.cooldown(3, 45, commands.BucketType.user)
    async def blur(self, ctx: commands.Context, user: Optional[discord.Member] = None, intensity: Optional[int] = 5):
        user = user or ctx.author
        if intensity > 25 or intensity < -25:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}The blur intensity can't be greater than `25`")
        avatar_bytes = await user.display_avatar.replace(format='png', size=256).read()
        async with ctx.channel.typing():
            await ctx.reply(
                file=discord.File(await self.bot.loop.run_in_executor(None, functools.partial(effects.blur, avatar_bytes, intensity)))
            )



def setup(bot):
    bot.add_cog(Images(bot))