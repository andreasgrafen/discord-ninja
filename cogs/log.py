import discord

from discord.ext import commands



class Log (commands.Cog):


    def __init__ (self, bot):

        self.bot         = bot
        self.home_guild  = self.bot.home_guild
        self.log_channel = self.bot.get_channel(self.bot.log_channel)



    @commands.Cog.listener()
    async def on_raw_message_delete (self, payload):

        if payload.guild_id == self.home_guild:
            # ignore deleted messages calling the echo command
            p = self.bot.command_prefix
            if not payload.cached_message.content.startswith((f'{p}echo', f'{p}say', f'{p}repeat', f'{p}tell')):
                # ignore messages deleted by purge
                if not payload.cached_message.content.endswith('Messages deleted.'):
                    origin_channel = self.bot.get_channel(payload.channel_id)
                    await self.log_channel.send("**Message deleted**\n"
                                               f"Author: {payload.cached_message.author.mention}\n"
                                               f"Channel: {origin_channel.mention} ({payload.channel_id})\n"
                                               f"Message: {payload.cached_message.content}")





def setup (bot):
    bot.add_cog(Log(bot))
