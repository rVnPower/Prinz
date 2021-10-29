#####################################################
import discord
from discord.ext import commands, tasks
import random
import asyncio
import dateparser
import re

from contextlib import suppress
from discord.utils import sleep_until, escape_markdown
from discord.ext.commands.cooldowns import BucketType
from collections import Counter
from utils import default
from config import EMOJIS
#####################################################
async def perform_mute_wait(time):
        await sleep_until(time)

class Moderation(commands.Cog, description="A powerful banhammer", name="Moderation"):
    def __init__(self, bot):
        self.bot = bot

    async def _basic_cleanup_strategy(self, ctx, search):
        count = 0
        async for msg in ctx.history(limit=search, before=ctx.message):
            if msg.author == ctx.me:
                await msg.delete()
                count += 1
        return {'Bot': count}

    @staticmethod
    async def get_invite_for_reinvite(ctx: commands.Context, max_age: int = 86400):
        """Handles the reinvite logic for getting an invite
        to send the newly unbanned user
        :returns: :class:`Invite`"""
        guild = ctx.guild
        my_perms: discord.Permissions = guild.me.guild_permissions
        if my_perms.manage_guild or my_perms.administrator:
            if "VANITY_URL" in guild.features:
                # guild has a vanity url so use it as the one to send
                try:
                    return await guild.vanity_invite()
                except discord.NotFound:
                    # If a guild has the vanity url feature,
                    # but does not have it set up,
                    # this prevents the command from failing
                    # and defaults back to another regular invite.
                    pass
            invites = await guild.invites()
        else:
            invites = []
        for inv in invites:  # Loop through the invites for the guild
            if not (inv.max_uses or inv.max_age or inv.temporary):
                # Invite is for the guild's default channel,
                # has unlimited uses, doesn't expire, and
                # doesn't grant temporary membership
                # (i.e. they won't be kicked on disconnect)
                return inv
        else:  # No existing invite found that is valid
            channels_and_perms = zip(
                guild.text_channels, map(guild.me.permissions_in, guild.text_channels)
            )
            channel = next(
                (channel for channel, perms in channels_and_perms if perms.create_instant_invite),
                None,
            )
            if channel is None:
                return
            try:
                # Create invite that expires after max_age
                return await channel.create_invite(max_age=max_age)
            except discord.HTTPException:
                return

    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None):
        if limit > 2000:
            return await ctx.send(f"{EMOJIS['tick_no']} Limit exceeded by **{limit - 2000}**")

        if before is None:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after is not None:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden as e:
            return await ctx.send(f"{EMOJIS['tick_no']} Looks like I'm missing permissions!")
        except discord.HTTPException as e:
            return await ctx.send("{{EMOJIS['tick_no']} Error occured!\n`{e}`")
        except discord.errors.NotFound:
            return
        except Exception as e:
            return await ctx.send(f"{EMOJIS['tick_no']} Error occured!\n`{e}`")

        spammers = Counter(m.author.display_name for m in deleted)
        deleted = len(deleted)
        if deleted == 1:
            messages = ["Purged **1** message"]
        else:
            messages = ["Purged **{0}** messages".format(deleted)]
        if deleted:
            messages.append('')
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f'**{escape_markdown(name)}**: {count}' for name, count in spammers)

        to_send = '\n'.join(messages)

        if len(to_send) > 2000:
            await ctx.send("Purged **{0}** messages".format(deleted), delete_after=10)
        else:
            message = to_send
            await ctx.send(message, delete_after=10)



    @commands.command(aliases=['k'], help="Kick a member")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
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

    @commands.command(aliases=['b'], help="Ban a member")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
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
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Hey!")
        embed.add_field(name="I'm sorry about this but...", value=f" You have been banned from {ctx.guild.name} for {reason}!")
        await member.send(embed=embed)

    @commands.group(aliases=['clear', 'delete', 'prune'], brief="Manage messages in the chat", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def purge(self, ctx, search=100):
        """ Purge messages in the chat. Default amount is set to **100**. This will not purge pins. """

        with suppress(Exception):
            await ctx.message.delete()

        def pins(m):
            if not m.pinned:
                return True
            return False
        await self.do_removal(ctx, search, pins)

    @purge.command(brief="Purge all the messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def all(self, ctx, search=100):
        """ Purge all the messages in chat. Default amount is set to **100**. This will purge everything, pins as well. """

        with suppress(Exception):
            await ctx.message.delete()
        await self.do_removal(ctx, search, lambda e: True)

    @purge.command(brief="User messages", description="Clear messages sent from an user")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def user(self, ctx, member: discord.Member, search=100):
        """ Removes user messages """

        with suppress(Exception):
            await ctx.message.delete()
        await self.do_removal(ctx, search, lambda e: e.author == member)

    @purge.command(name='bot', brief="Clear bot user messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def _bot(self, ctx, prefix=None, search=100):
        """Removes a bot user's messages and messages with their optional prefix."""

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (prefix and m.content.startswith(prefix))

        await self.do_removal(ctx, search, predicate)

    @purge.command(brief="Clear embedded messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""

        await self.do_removal(ctx, search, lambda e: len(e.embeds))

    @purge.command(brief="Clear messages with images")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @purge.command(brief="Messages containing the given word")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def contains(self, ctx, *, substr: str):
        """ Removes all messages containing a substring. The substring must be at least 3 characters long. """
        if len(substr) < 3:
            await ctx.send(f"{EMOJIS['tick_no']} substring must be at least 3 characters long.")
        else:
            await self.do_removal(ctx, 100, lambda e: substr in e.content)

    @purge.command(name='emoji', brief="Delete custom emoji messages")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.max_concurrency(1, commands.cooldowns.BucketType.channel, wait=False)
    async def _emoji(self, ctx, search=100):
        """Removes all messages containing custom emoji."""
        custom_emoji = re.compile(r'<:(\w+):(\d+)>')

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(ctx, search, predicate)

    @commands.command(aliases=['u'], help="Unban an user")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Successfully unbanned {user.mention}!")
            else:
                await ctx.send("Maybe that user doesn't exist...")

    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=['bl'], help="Show the banned users list")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def banlist(self, ctx):
        banned_users = await ctx.guild.bans()
        await ctx.send(banned_users)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['m'], help='Mute an user')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        author = ctx.author
        embed = discord.Embed(colour=discord.Colour.blurple())        
        if author == member:
            embed.set_author(name=f"I can't let you do that {ctx.author}!")
            await ctx.send(embed=embed)
            return
        muteRole = discord.utils.get(guild.roles, name="Muted")

        if not muteRole:
            embed.set_author(name="No mute role found. Creating one...")
            await ctx.send(embed=embed)
            muteRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=False)
        await member.add_roles(muteRole, reason=reason)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=f'Successfully muted {member.mention}!')
        await ctx.send(embed=embed, delete_after=10)
        embed = discord.Embed(colour=discord.Colour.blurple(), title=f"You have been muted from {guild.name}!", description=f"Reason: {reason}")
        await member.send(embed=embed)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['um'], help='Unmute an user')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        author = ctx.author
        embed = discord.Embed(colour=discord.Colour.blurple())
        muteRole = discord.utils.get(guild.roles, name="Muted")

        if not muteRole:
            embed.set_author(name="No mute role found.")
            await ctx.send(embed=embed)
            return
        await member.remove_roles(muteRole, reason=reason)

        embed = discord.Embed(colour=discord.Colour.blurple(), description=f'Successfully unmuted {member.mention}!')
        await ctx.send(embed=embed, delete_after=10)
        embed = discord.Embed(colour=discord.Colour.blurple(), title=f"You have been unmuted from {guild.name}!", description=f"Reason: {reason}")
        await member.send(embed=embed)

    @commands.has_permissions(manage_roles=True)
    @commands.command(help='Add a role to a member')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def add_role(self, ctx, member:discord.Member, *, roleName, reason=None):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        try:
            await member.add_roles(role, reason=reason)
        except AttributeError:
            try:
                role = ctx.guild.get_role(int(roleName))
            except AttributeError:
                role = ctx.guild.get_role(int(roleName[3: len(roleName)-1]))
            await member.add_roles(role, reason=reason)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=f"Successfully gave {role.mention} role to {member}!")
        await ctx.send(embed=embed, delete_after=10)

    @commands.has_permissions(manage_roles=True)
    @commands.command(help='Remove a role from a member')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove_role(self, ctx, member:discord.Member, *, roleName, reason=None):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        try:
            await member.remove_roles(role, reason=reason)
        except AttributeError:
            try:
                role = ctx.guild.get_role(int(roleName))
            except ValueError:
                role = ctx.guild.get_role(int(roleName[3: len(roleName)-1]))
            await member.remove_roles(role, reason=reason)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=f"Successfully removed {role.mention} role to {member}!")
        await ctx.send(embed=embed, delete_after=10)

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Kick an user and delete messenges from that user for 1 day")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def softban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        ''' Kick an user and delete messenges from that user for 1 day'''
        guild = ctx.guild
        author = ctx.author
        embed = discord.Embed(colour=discord.Colour.blurple())
        if author == member:
            embed.set_author(name=f"I can't let you do that {ctx.author}!")
            await ctx.send(embed=embed)
            return

        invite = await self.get_invite_for_reinvite(ctx)
        if invite is None:
            invite = ""

        try:
            msg = await member.send(embed=discord.Embed(colour=discord.Colour.blurple(), title="You have been banned then unbanned as a quick way to delete your messenges.", description=f"You can now join the server again: {invite}"))
        except discord.HTTPException:
            msg = None
        try:
            await guild.ban(member, reason=reason, delete_message_days=1)
        except discord.errors.Forbidden:
            await ctx.send("My role is not high enough to softban that user.")
            if msg is not None:
                await msg.delete()
            return
        try:
            await guild.unban(member)
        except:
            await ctx.send("An error ocurred.")
        else:
            await ctx.send(f'Done.')

    @commands.command(help="Clean up the bot's messages")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    async def cleanup(self, ctx, search=100):
        """ Cleans up the bot's messages from the channel.
        If the bot has Manage Messages permissions then it will try to delete messages that look like they invoked the bot as well. """

        strategy = self._basic_cleanup_strategy
        if ctx.me.permissions_in(ctx.channel).manage_messages:
            strategy = self._complex_cleanup_strategy

        spammers = await strategy(ctx, search)
        deleted = sum(spammers.values())
        messages = ['{0} message was removed.'.format(deleted) if deleted == 1 else '{0} messages were removed.'.format(deleted)]
        if deleted:
            messages.append('\nTotal messages by user:')
            spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
            messages.extend(f'- **{author}**: {count}' for author, count in spammers)

        await ctx.send('\n'.join(messages))

    @commands.command(brief='Nuke the channel')
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.member)

    async def nuke(self, ctx, channel: discord.TextChannel = None, *, reason: commands.clean_content = None):
        """ Nuke any server in the channel. This command will clone the selected channel and create another one with exact permissions """

        channel = channel or ctx.channel
        reason = reason or None

        try:
            new_channel = await channel.clone(reason=default.responsible(ctx.author, reason))
            await new_channel.edit(position=channel.position)
            await new_channel.send(f"{EMOJIS['tick_yes']} This channel got nuked by {ctx.author.mention}!", delete_after=15)
            await channel.delete()
        except Exception as e:

            return await ctx.send("{0} Something failed with sending the message, I've sent this error to my developers and they should hopefully resolve it soon.".format(EMOJIS['tick_no']))

    @commands.command(brief="Freeze the server", aliases=['freeze-server'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def freeze(self, ctx, reason: str = None):
        """ Freezes everyone from sending messages in the server """

        permissions = ctx.guild.default_role.permissions
        if permissions.send_messages:
            permissions.update(send_messages=False)
            permissions.update(connect=False)
            await ctx.guild.default_role.edit(permissions=permissions, reason=default.responsible(ctx.author, reason))
            try:
                await ctx.send("{0} Server is now frozen!".format(EMOJIS['snowflake']))
            except Exception:
                await ctx.message.add_reaction(f"{EMOJIS['snowflake']}")
        elif not permissions.send_messages:
            await ctx.send("{0} Server is already frozen!".format(EMOJIS['tick_no']))

    @commands.command(brief="Unfreeze the server", aliases=['unfreeze-server'])
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def unfreeze(self, ctx, reason: str = None):
        """ Unfreezes everyone from sending messages in the server """

        permissions = ctx.guild.default_role.permissions

        if not permissions.send_messages:
            permissions.update(send_messages=True)
            permissions.update(connect=True)
            await ctx.guild.default_role.edit(permissions=permissions, reason=default.responsible(ctx.author, reason))
            try:
                await ctx.send("{0} Server is now unfrozen!".format(EMOJIS['tick_yes']))
            except Exception:
                await ctx.message.add_reaction(f"{EMOJIS['snowflake']}")
        elif permissions.send_messages:
            await ctx.send("{0} Server is not frozen!".format(EMOJIS['tick_no']))


def setup(bot):
    bot.add_cog(Moderation(bot))