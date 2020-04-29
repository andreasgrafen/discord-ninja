import random
import discord

from discord.ext import commands



class RNG (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot


    def get_online_users (self, member_list):

        online = []

        for u in member_list:
            if u.status == discord.Status.online and u.bot == False:
                online.append(u)

        return online



    @commands.group(name = 'random', aliases = ['rng', 'lucky'])
    async def random (self, ctx):

        """Who doesn't love some RNG?"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @random.command(name = 'user', aliases = ['person'])
    @commands.guild_only()
    async def random_user (self, ctx):

        """Returns a random online user."""

        online_users = self.get_online_users(ctx.guild.members)
        random_user  = random.choice(online_users)

        if ctx.channel.permissions_for(ctx.author).mention_everyone:
            winner = random_user.mention

        else:
            winner = random_user.display_name

        await ctx.send(f"And the winner is **{winner}**!")



    @random.command(name = 'choice', aliases = ['list'])
    async def random_choice (self, ctx, *choices: str):

        """Returns a value from provided choices."""

        all_choices = list(choices)
        all_choices.pop(0) # remove the "choice" keyword
        winner = random.choice(all_choices)
        await ctx.send(f"The winning option is **{winner}**.")



    @random.command(name = 'number', aliases = ['#'])
    async def random_number (self, ctx, min: int = 0, max: int = 100):

        """Returns a random number.
        You can provide your own min/max values as argument.
        Otherwise it will default to 0 to 100."""

        await ctx.send(random.randint(min, max))





def setup (bot):
    bot.add_cog(RNG(bot))
