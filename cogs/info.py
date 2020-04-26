import time
import discord
import datetime

from discord.ext import commands



class Info (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.command(name = 'ping', aliases = ['latency', 'connection', 'conn', 'pong'])
    async def get_ping (self, ctx):

        """Pong! See the bots latency."""

        before = time.monotonic()
        msg    = await ctx.send("Pong!")
        ping   = (time.monotonic() - before) * 1000
        await msg.edit(content = f"My latency is {int(ping)}ms.")



    @commands.command(name = 'uptime', aliases = ['onlinetime', 'alive'])
    async def get_uptime (self, ctx):

        """Tells you how long the bot has been up for."""

        uptime_complete = datetime.datetime.utcnow() - self.bot.uptime
        uptime_parts    = str(uptime_complete).split(':')
        uptime_hours     = uptime_parts[0]
        uptime_minutes   = uptime_parts[1]
        uptime_seconds   = uptime_parts[2].split('.')[0]

        await ctx.send(f"**Uptime:** {uptime_hours} hours, {uptime_minutes} minutes and {uptime_seconds} seconds.")



    @commands.command(name = 'invite', aliases = ['join', 'joinme', 'inviteme', 'invitebot'])
    async def invite_me (self, ctx):

        """Invite the bot to your server.
        This command will create a Discord oAuth link."""

        await ctx.send("Use this URL to invite me to your server."
                      f"{discord.utils.oauth_url(self.bot.user.id)}")



    @commands.command(name = 'serverinfo', aliases = ['guildinfo'])
    @commands.guild_only()
    async def guild_info (self, ctx):

        """See metadata for the current server."""

        guild          = ctx.guild
        text_channels  = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles          = []

        roles.extend([role.mention for role in guild.roles[1:]])
        roles = ', '.join(roles)

        e = discord.Embed(title = 'Server Info', colour = 0xb8e994)
        e.set_author(icon_url = guild.icon_url, name = guild.name)

        e.add_field(name = 'ID',            value = guild.id)
        e.add_field(name = 'Owner',         value = guild.owner)
        e.add_field(name = 'Region',        value = guild.region)
        e.add_field(name = 'Members',       value = guild.member_count)
        e.add_field(name = 'Textchannels',  value = text_channels)
        e.add_field(name = 'Voicechannels', value = voice_channels)
        e.add_field(name = 'Created',       value = guild.created_at.isoformat(" ", "seconds"))
        e.add_field(name = 'Roles',         value = roles)

        await ctx.send(embed = e)



    @commands.command(name = 'avatar', aliases = ['ava', 'pfp', 'picture'])
    @commands.guild_only()
    async def get_avatar (self, ctx, *, member: discord.Member = None):

        """Grabs the avatar of a user.
        Defaults to the author if no user is specified."""

        if not member:
            member = ctx.author

        avatar_url = member.avatar_url_as(static_format = 'png')

        e = discord.Embed(colour = member.colour)
        e.set_author(name = member.display_name, url = avatar_url)
        e.set_image(url = avatar_url)

        await ctx.send(embed = e)



    @commands.command(name = 'joined', aliases = ['since', 'age'])
    @commands.guild_only()
    async def join_date (self, ctx, *, member : discord.Member = None):

        """Looks up when a member joined the server.
        Defaults to the author if no user is specified."""

        if not member:
            member = ctx.author

        await ctx.send(f"{member.display_name} joined on **{member.joined_at.isoformat(' ', 'seconds')}**.")



    @commands.command(name = 'spotify', alias = ['music', 'listening'])
    @commands.guild_only()
    async def get_spotify_status (self, ctx, member: discord.Member = None):

        """Get the current song a user is listening to."""

        if member is None:
            member     = ctx.author

        activity = member.activity

        if activity is None:
            await ctx.send(f"{member.display_name} isn't playing anything on Spotify right now.")
            return

        if activity.type == discord.ActivityType.listening and activity.name == 'Spotify':
            e                    = discord.Embed(description = '\u200b')
            e.add_field(name     = 'Artist', value = ', '.join(activity.artists))
            e.add_field(name     = 'Album', value = activity.album)
            e.add_field(name     = 'Duration', value = str(activity.duration)[3:].split('.', 1)[0])
            e.title              = f'**{activity.title}**'
            e.set_thumbnail(url  = activity.album_cover_url)
            e.url                = f'https://open.spotify.com/track/{activity.track_id}'
            e.colour             = activity.colour
            e.set_footer(text    = f'{member.display_name} is currently playing this song.')
            await ctx.send(embed = e)

        else:
            await ctx.send(f"{member.display_name} isn't playing anything on Spotify right now.")





def setup (bot):
    bot.add_cog(Info(bot))
