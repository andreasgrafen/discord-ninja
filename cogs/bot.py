import time
import discord
import datetime

from discord.ext import commands



class Bot (commands.Cog):


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



    @commands.command(name = 'source', aliases = ['code', 'sourcecode', 'github'])
    async def send_github_link (self, ctx):

        """Get a link to the bots GitHub repository."""

        await ctx.send(f"{ctx.bot.user.mention} is powered by this mess of random characters:\nhttps://andreas.grafen.info/github/discord-ninja")





def setup (bot):
    bot.add_cog(Bot(bot))
