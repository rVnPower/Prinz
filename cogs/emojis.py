import discord
from discord.ext import commands

from typing import Union

from utils.embed import error_embed, success_embed
from utils.ui import Confirm
from config import EMOJIS, MAIN_COLOR

class Emojis(commands.Cog):
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

    @commands.command(help="Clone emojis!", aliases=['clone-emoji', 'cloneemoji'])
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

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        # checking if nqn is enabled or not
        guild_config = await self.bot.get_guild_config(message.guild.id)
        if not guild_config['nqn']:
            return
        # checking for blacklisted users
        for e in self.bot.blacklisted_cache:
            if message.author.id == e['_id']:
                return
        # spliting the message content
        pain = message.content.split(" ")

        # empty string that i'll fill with cu- i mean the final nqn output text
        final_msg = ""
        # am iterating thru every single word in the list `pain`
        for e in pain:
            # spliting the word with ":" for checking if it has emoji or not
            hmm = e.split(":")

            # if it had emoji it would have 2 `:` in the word which means the lenght of `hmm` would atleast be `3` and if its not 3 then we dont do anything
            if len(hmm) < 3:
                final_msg += e + " "
            # it has 2 or more `:` in the word so it has chances of having `:something:` in it
            else:
                i = 1
                # another empty string that im gonna fill with cu- i mean text!
                interesting = ""
                for h in range(0, len(hmm)):
                    ee = hmm[h]
                    # now over here im checking if the word that im replacing with the emoji is in between the 2 `:`'s

                    # like when i split "amogus:some_emoji:amogus" i will get ["amogus", "some_emoji", "amogus"]
                    # so im making sure that i replace "some_emoji" with the actual emoji string
                    if i % 2 == 0:
                        # finding the emoji...
                        emoji = discord.utils.get(self.bot.emojis, name=ee)
                        # here im checking if the actual word contains a nitro emoji or a fake emoji

                        # by nitro emoji i mean "<:emoji_name:ID>" and by fake emoji i mean ":emoji_name:"
                        # we only want to replace if it contains a fake emoji and not a real emoji
                        if emoji is not None and emoji.is_usable() and (hmm[h + 1][18: 19] != ">"):
                            interesting += str(emoji)
                        else:
                            interesting += ":" + ee + (":" if len(hmm) != i else "")
                    else:
                        interesting += ee
                    i += 1
                final_msg += interesting + " "
        if final_msg not in [message.content, message.content[:-1], message.content + " "]:
            msg_attachments = []
            for attachment in message.attachments:
                uwu = await attachment.to_file()
                msg_attachments.append(uwu)
            await message.delete()
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="EpicBot NQN", user=self.bot.user)
            if webhook is None:
                webhook = await message.channel.create_webhook(name="EpicBot NQN")

            await webhook.send(
                final_msg,
                files=msg_attachments,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none()
            )

def setup(bot):
    bot.add_cog(Emojis(bot))