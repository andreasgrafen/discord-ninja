import discord

from discord.ext import commands



class Moderation (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.command(name = 'echo', aliases = ['say', 'tell'])
    @commands.has_permissions(administrator = True)
    @commands.guild_only()
    async def echo (self, ctx, *, content: str):

        """Repeats a given message."""

        try:
            await ctx.channel.purge(limit = 1) # remove the message invoking this command

        except:
            pass

        await ctx.send(content)



    @commands.group(name = 'purge', aliases = ['clear', 'remove', 'prune'])
    @commands.has_permissions(manage_messages = True)
    @commands.guild_only()
    async def purge (self, ctx):

        """Purge (specific) messages."""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @purge.command(name = 'all')
    async def purge_all (self, ctx, limit: int = 10):

        """Purge a specified ammount of messages."""

        deleted = 0
        while limit >= 1:
            cap = min(limit, 100)
            deleted += len(await ctx.channel.purge(limit = cap))
            limit -= cap

        await ctx.send(content = f":put_litter_in_its_place: {deleted} Messages deleted.", delete_after = 10)



    @purge.command(name = 'user')
    async def purge_user (self, ctx, member: discord.Member, limit: int = 10):

        """Purge X messages from a specified user."""

        try:
            await ctx.channel.purge(limit = limit, check = lambda e: e.author == member)
            await ctx.send(content = f":put_litter_in_its_place: {limit} Messages from {member.mention} deleted.", delete_after = 10)

        except Exception as e:
            await ctx.send(e)



    @commands.command(name = 'nickname', aliases = ['nick'])
    @commands.has_permissions(manage_nicknames = True)
    @commands.guild_only()
    async def change_user_nick (self, ctx, member: discord.Member, *, new_nick: str = None):

        """Change a nickname.
        To reset a nickname leave the argument blank."""

        try:
            await member.edit(nick = new_nick)
            msg = f"Successfully changed **{member.name}'s** nickname to {member.mention}"

            if new_nick is None:
                msg = f"Successfully reset {member.mention}'s nickname."

            await ctx.send(msg)

        except Exception as e:
            await ctx.send(e)





def setup (bot):

    bot.add_cog(Moderation(bot))
