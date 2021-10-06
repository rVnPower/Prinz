import asyncio

import discord
from discord.ext.commands import Paginator as CommandPaginator
from discord.ext import commands


class CannotPaginate(Exception):
    pass


class Pages:
    """Implements a paginator that queries the user for the
    pagination interface.
    Pages are 1-index based, not 0-index based.
    If the user does not reply within 1 minute then the pagination
    interface exits automatically.
    Parameters
    ------------
    ctx: Context
        The context of the command.
    entries: List[str]
        A list of entries to paginate.
    per_page: int
        How many entries show up per page.
    show_entry_count: bool
        Whether to show an entry count in the footer.
    Attributes
    -----------
    embed: discord.Embed
        The embed object that is being used to send pagination info.
        Feel free to modify this externally. Only the description,
        footer fields, and colour are internally modified.
    permissions: discord.Permissions
        Our permissions for the channel.
    """
    def __init__(self, ctx, *, entries, per_page=12, show_entry_count=True, embed_color=discord.Color.blurple(), title=None, thumbnail=None, footericon=None, footertext=None, author=None, delete_after=None, embed_author=None, home=None):
        self.bot = ctx.bot
        self.entries = entries
        self.message = ctx.message
        self.channel = ctx.channel
        self.context = ctx
        self.author = author if author else ctx.author
        self.thumbnail = thumbnail
        self.footericon = footericon
        self.footertext = footertext
        self.home = home
        self.title = title
        self.embed_author = embed_author
        self.delete_after = 300
        self.per_page = per_page
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.embed = discord.Embed(colour=embed_color)
        self.paginating = True
        self.show_entry_count = show_entry_count
        self.reaction_emojis = [
            ('<:arrowleft:820332901559173150>', self.first_page),
            ('<:arrleft:820332933893586985>', self.previous_page),
            ('<:stop:820332883470319637>', self.stop_pages),
            ('<:arrright:820332951518445619>', self.next_page),
            ('<:arrowright:820332915795034123>', self.last_page),
            ('\U0001f3d8', self.main_help)
            # ('<:python:682881809649762358>', self.show_help)
        ]

        if ctx.guild is not None:
            self.permissions = self.channel.permissions_for(ctx.guild.me)
        else:
            self.permissions = self.channel.permissions_for(ctx.bot.user)

        if not self.permissions.embed_links:
            raise commands.BotMissingPermissions(['embed_links'])

        if not self.permissions.send_messages:
            raise commands.BotMissingPermissions('Bot cannot send messages.')

        if self.paginating:
            # verify we can actually use the pagination session
            if not (self.permissions.add_reactions or self.permissions.use_external_emojis):
                raise commands.BotMissingPermissions('I do not have permissions to add reactions.')

            if not self.permissions.read_message_history:
                raise commands.BotMissingPermissions('I do not have permissions to Read Message History.')

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    def get_content(self, entries, page, *, first=False):
        return None

    def get_embed(self, entries, page, *, first=False):
        self.prepare_embed(entries, page, first=first)
        return self.embed

    def prepare_embed(self, entries, page, *, first=False):
        p = []
        for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
            p.append(f'{entry}')

        if self.maximum_pages > 1 and not self.footertext:
            if self.show_entry_count:
                text = f'Showing page {page}/{self.maximum_pages} ({len(self.entries)} entries)'
            else:
                text = f'Showing page {page}/{self.maximum_pages}'

            self.embed.set_footer(text=text)

        if self.footertext:
            self.embed.set_footer(text=self.footertext)

        if self.paginating and first:
            p.append('')

        self.embed.description = ''.join(p)
        self.embed.title = self.title or discord.Embed.Empty
        if self.thumbnail:
            self.embed.set_thumbnail(url=self.thumbnail)
        if self.embed_author:
            self.embed.set_author(icon_url=self.author.avatar_url, name=self.embed_author)

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)
        content = self.get_content(entries, page, first=first)
        embed = self.get_embed(entries, page, first=first)

        if not first:
            await self.message.edit(content=content, embed=embed)
            return

        self.message = await self.channel.send(content=content, embed=embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('<:arrowleft:820332901559173150>', '<:arrowright:820332915795034123>'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue
            if not self.home and reaction in ('\U0001f3d8'):
                continue

            if self.maximum_pages == 1 and reaction in ('<:arrowleft:820332901559173150>', '<:arrowright:820332915795034123>', '<:arrleft:820332933893586985>', '<:arrright:820332951518445619>'):
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """goes to the first page"""
        await self.show_page(1)

    async def last_page(self):
        """goes to the last page"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """goes to the next page"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """goes to the previous page"""
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def main_help(self):
        """ Goes to the main page of help """
        await self.stop_pages()
        await self.context.send_help()

    async def numbered_page(self):
        """lets you type a page number to go to"""
        to_delete = []
        to_delete.append(await self.channel.send('What page do you want to go to?'))

        def message_check(m):
            return m.author == self.author and \
                self.channel == m.channel and \
                m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await self.channel.send('Took too long.'))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(await self.channel.send(f'Invalid page given. ({page}/{self.maximum_pages})'))
                await asyncio.sleep(5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """shows this message"""
        messages = ['Welcome to the interactive paginator!\n']
        messages.append('This interactively allows you to see pages of text by navigating with '
                        'reactions. They are as follows:\n')

        embed = self.embed.copy()
        embed.clear_fields()
        embed.description = '\n'.join(messages)
        embed.set_footer(text='We were on page before this message.')
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """stops the interactive pagination session"""
        await self.message.delete()
        self.paginating = False

    def react_check(self, reaction, user):
        if user is None or user.id != self.author.id and user.id != 345457928972533773:
            return False

        if reaction.message.id != self.message.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if str(reaction.emoji) == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        first_page = self.show_page(1, first=True)
        # allow us to react to reactions right away if we're paginating
        self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=self.delete_after)
            except asyncio.TimeoutError:
                self.paginating = False
                try:
                    await self.message.delete()
                except Exception:
                    pass
                finally:
                    break
            try:
                await self.message.remove_reaction(reaction, user)
            except Exception:
                pass  # can't remove it so don't bother doing so

            await self.match()