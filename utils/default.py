import discord
import time
import traceback
from datetime import datetime, timezone, timedelta

def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = '```py\n{1}{0}: {2}\n```'.format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"

async def background_error(ctx, err_type, err_msg, guild, channel):
    message = f"{ctx.bot.settings['emojis']['misc']['error']} **Error occured on event -** " \
              f"{err_type}"
    e = discord.Embed(color=ctx.bot.settings['colors']['error_color'], timestamp=datetime.now(timezone.utc))
    e.description = traceback_maker(err_msg)
    e.add_field(name="Server it occured in:", value=f"**Server:** {guild} ({guild.id})\n"
                                                    f"**Channel:** #{channel} ({'' if not channel else channel.id})")
    channel = ctx.bot.get_channel(ctx.bot.settings['channels']['event-errors'])
    return await channel.send(content=message, embed=e)

async def spotify_support(ctx, spotify, search_type, spotify_id, Track, Player) -> None:
    player = ctx.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
    spotify_client = spotify.Client(ctx.bot.config.SPOTIFY_CLIENT, ctx.bot.config.SPOTIFY_SECRET)
    spotify_http_client = spotify.HTTPClient(ctx.bot.config.SPOTIFY_CLIENT, ctx.bot.config.SPOTIFY_SECRET)

    if search_type == "playlist":
        results = spotify.Playlist(client=spotify_client, data=await spotify_http_client.get_playlist(spotify_id))
        try:
            search_tracks = await results.get_all_tracks()
        except Exception:
            return await ctx.send("I was not able to find this playlist! Please try again or use a different link.")

    elif search_type == "album":
        results = await spotify_client.get_album(spotify_id=spotify_id)
        try:
            search_tracks = await results.get_all_tracks()
        except Exception:
            return await ctx.send("I was not able to find this album! Please try again or use a different link.")

    elif search_type == 'track':
        results = await spotify_client.get_track(spotify_id=spotify_id)
        search_tracks = [results]

    tracks = [
        Track('spotify',
              {
                  'title': track.name or 'Unknown', 'author': ', '.join(artist.name for artist in track.artists) or 'Unknown',
                  'length': track.duration or 0, 'identifier': track.id or 'Unknown', 'uri': track.url or 'spotify',
                  'isStream': False, 'isSeekable': False, 'position': 0, 'thumbnail': track.images[0].url if track.images else None
              },
              requester=ctx.author,
              ) for track in search_tracks
    ]

    if not tracks:
        return await ctx.send("The URL you put is either not valid or doesn't exist!")

    if search_type == "playlist":
        for track in tracks:
            player.queue.put_nowait(track)

        await ctx.send('{0} Added the playlist **{1}**'
                         ' with {2} songs to the queue!', delete_after=15).format('🎶', results.name, len(tracks))
    elif search_type == "album":
        for track in tracks:
            player.queue.put_nowait(track)

        await ctx.send('{0} Added the album **{1}**'
                         ' with {2} songs to the queue!', delete_after=15).format('🎶', results.name, len(tracks))
    else:
        if player.is_playing:
            await ctx.send('{0} Added **{1}** to the Queue!', tracks[0].title, delete_after=15).format('🎶')
        player.queue.put_nowait(tracks[0])

    if not player.is_playing:
        await player.do_next()