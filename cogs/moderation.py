#####################################################
import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta, timezone
import contextlib
import dateparser # a converter that converts string to datetime, None otherwise, use another if you want
from discord.utils import sleep_until
import asyncio
#####################################################
async def perform_mute_wait(time):
        await sleep_until(time)

class Moderation(commands.Cog, description="Moderation commands"):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(aliases=['k'], description="Kick a member")
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

    @commands.command(aliases=['b'], description="Ban a member")
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
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name="Hey!")
        embed.add_field(name="I'm sorry about this but...", value=f" You have been banned from {ctx.guild.name} for {reason}!")
        await member.send(embed=embed)

    @commands.command(aliases=['d'], description="Clear a number of messages")
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command(aliases=['u'], description="Unban an user")
    @commands.has_permissions(ban_members=True)
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
    @commands.command(aliases=['bl'], description="Show the banned users list")
    async def banlist(self, ctx):
        banned_users = await ctx.guild.bans()
        await ctx.send(banned_users)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['m'], description='Mute an user')
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
    @commands.command(aliases=['um'], description='Unmute an user')
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
    @commands.command(description='Add a role to a member')
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
    @commands.command(description='Remove a role from a member')
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

    # @commands.has_permissions(ban_members=True)
    @commands.is_owner()
    @commands.command(description="Kick an user and delete messenges from that user for 1 day")
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

    @commands.has_permissions(manage_messages=True)
    @commands.command(usage="tempmute \"1d 2s\" @User [reason]")
    async def tempmute(self, ctx, member: discord.Member, *, time: str, reason: str = None):
        embed = discord.Embed(colour=discord.Colour.blurple())
        time = dateparser.parse(time)
        if time is None:
            embed.set_author(name="Invaild time.")
            return

        muteRole = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muteRole:
            embed.set_author(name="No mute role found. Creating one...")
            await ctx.send(embed=embed)
            muteRole = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=False)
  
        await member.add_roles(muteRole)
        embed = discord.Embed(colour=discord.Colour.blurple(), description=f"{member.mention} has been muted and will be Back in <t:{round(time.timestamp())}>")
        await ctx.send(embed=embed)
        loop = ctx.bot.loop
        loop.create_task(perform_mute_wait(time))
'''
    @commands.command()
    async def tempban(self, ctx: commands.Context, member: discord.Member, duration: Optional[commands.TimedeltaConverter] = None, days: Optional[int] = None,*,reason: str = None):
        """Temporarily ban a user from this server.
        `duration` is the amount of time the user should be banned for.
        `days` is the amount of days of messages to cleanup on tempban.
        Examples:
           - `[p]tempban @Twentysix Because I say so`
            This will ban Twentysix for the default amount of time set by an administrator.
           - `[p]tempban @Twentysix 15m You need a timeout`
            This will ban Twentysix for 15 minutes.
           - `[p]tempban 428675506947227648 1d2h15m 5 Evil person`
            This will ban the user for 1 day 2 hours 15 minutes and will delete the last 5 days of their messages.
        """
        guild = ctx.guild
        author = ctx.author
        embed = discord.Embed(colour=discord.Colour.blurple())
        if author == member:
            embed.set_author(name=f"I can't let you do that {author.mention}!")
            await ctx.send(embed=embed)
            return
        elif guild.me.top_role <= member.top_role or member == guild.owner:
            await ctx.send("I cannot do that due to Discord hierarchy rules.")
            return

        if duration is None:
            duration = timedelta(seconds=await self.config.guild(guild).default_tempban_duration())
        unban_time = datetime.now(timezone.utc) + duration

        if days is None:
            days = await self.config.guild(guild).default_days()
        if not (0 <= days <= 7):
            await ctx.send("Invaild days. Days must be between 0 and 7.")
        invite = await self.get_invite_for_reinvite(ctx, int(duration.total_seconds() + 86400))
        if invite is None:
            invite = ""
'''
def setup(bot):
    bot.add_cog(Moderation(bot))