import discord
from discord.ext import commands

import aiohttp
from typing import Union

from utils.embed import error_embed, success_embed
from utils.ui import Confirm
from config import EMOJIS, MAIN_COLOR

class Emojis(commands.Cog, description="Things with emojis"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(help="Enlarge an emoji.")
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        prefix = ctx.clean_prefix
        if emoji is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter an emoji to enlarge.\nCorrect Usage: `{prefix}enlarge <emoji>`"
            ))
        if isinstance(emoji, str):
            raise commands.EmojiNotFound(emoji)
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(emoji.url)

    @commands.command(help="Clone emojis! (Thanks to EpicBot)", aliases=['clone-emoji', 'cloneemoji'])
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def clone(self, ctx, emojis: commands.Greedy[Union[discord.PartialEmoji, discord.Emoji]] = None):
        prefix = ctx.clean_prefix
        if emojis is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter some emojis to clone.\n\n**Example:** {prefix}clone {EMOJIS['heart']} {EMOJIS['flushed']} ..."
            ))
        uploaded_emojis = ""
        failed_emojis = ""

        m = await ctx.reply(f"Cloning emojis... {EMOJIS['loading']}")

        for emoji in emojis:
            if isinstance(emoji, discord.PartialEmoji):
                try:
                    emo = await ctx.guild.create_custom_emoji(
                        name=emoji.name,
                        image=await emoji.read(),
                        reason=f"Clone command used by {ctx.author} ({ctx.author.id})"
                    )
                    uploaded_emojis += f"{emo} "
                except Exception:
                    failed_emojis += f"`{emoji.name}` "
            else:
                view = Confirm(context=ctx)
                await m.edit(
                    content="",
                    embed=success_embed(
                        "Is this the emoji you wanted?",
                        f"The name `{emoji.name}` corresponds to this emote, do you want to clone this?"
                    ).set_image(url=emoji.url),
                    view=view
                )
                await view.wait()
                if view.value is None:
                    await m.edit(
                        content="",
                        embed=error_embed(
                            "You didn't respond in time.",
                            f"Skipped this emoji. Cloning other emojis... {EMOJIS['loading']}"
                        ),
                        view=None
                    )
                elif not view.value:
                    await m.edit(
                        content="",
                        embed=success_embed(
                            f"{EMOJIS['tick_yes']} Alright!",
                            "Skipped that emoji."
                        ),
                        view=None
                    )
                else:
                    await m.edit(
                        content="",
                        embed=discord.Embed(
                            title=f"{EMOJIS['tick_yes']} Ok, cloning...",
                            color=MAIN_COLOR
                        ),
                        view=None
                    )
                    try:
                        emo = await ctx.guild.create_custom_emoji(
                            name=emoji.name,
                            image=await emoji.read(),
                            reason=f"Clone command used by {ctx.author} ({ctx.author.id})"
                        )
                        uploaded_emojis += f"{emo} "
                    except Exception:
                        failed_emojis += f"`{emoji.name}` "

        await m.edit(
            content=f"Successfully cloned {uploaded_emojis}{' and failed to clone '+failed_emojis if len(failed_emojis) > 0 else ''}",
            embed=None,
            view=None
        )

    @commands.command(help="Create an emoji", aliases=['cemoji', 'createemoji'], name='create-emoji')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def createemoji(self, ctx, emoji_url: str, *, emoji_name: str):
        """ Create an emoji """

        if len(emoji_name) > 32:
            raise commands.BadArgument("Emoji name can't be longer than 32 characters, you're {0} characters over".format(len(emoji_name) - 32))

        if len(ctx.guild.emojis) >= ctx.guild.emoji_limit:
            raise commands.BadArgument("This guild has reached the max amount of emojis added.")

        try:
            async with aiohttp.ClientSession() as c:
                async with c.get(emoji_url) as f:
                    bio = await f.read()

            emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=bio)
            await ctx.send("{0} Successfully created {1} emoji in this server.".format(EMOJIS['tick_yes'], emoji))
        except aiohttp.InvalidURL:
            await ctx.send("Emoji URL is invalid")
        except discord.InvalidArgument:
            await ctx.send("The URL doesn't contain any image")
        except discord.HTTPException as err:
            await ctx.send(err)
        except TypeError:
            await ctx.send("You need to either provide an image URL or upload one with the command")

def setup(bot):
    bot.add_cog(Emojis(bot))