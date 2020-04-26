import discord

from discord.ext import commands



class Moderation (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.command(name = 'echo', aliases = ['say', 'tell'])
    @commands.has_permissions(administrator = True)
    async def echo (self, ctx, *, content: str):

        """Repeats a given message."""

        try:
            await ctx.channel.purge(limit = 1) # remove the message invoking this command

        except:
            pass

        await ctx.send(content)



    @commands.command(name = 'purge', aliases = ['clear', 'remove', 'prune'])
    @commands.has_permissions(manage_messages = True)
    async def purge_messages (self, ctx, *limit):

        """Purge a specified ammount of messages."""

        try:
            limit = int(limit[0])

        except IndexError:
            limit = 1

        deleted = 0
        while limit >= 1:
            cap = min(limit, 100)
            deleted += len(await ctx.channel.purge(limit = cap))
            limit -= cap

        await ctx.send(content = f":put_litter_in_its_place: {deleted} Messages deleted.", delete_after = 10)



    @commands.command(name = 'nickname', aliases = ['nick'])
    @commands.has_permissions(manage_nicknames = True)
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
