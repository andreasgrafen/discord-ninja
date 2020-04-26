import random
import aiohttp
import discord

from discord.ext import commands



class Fun (commands.Cog):


    def __init__ (self, bot):

        self.bot            = bot
        self.session        = aiohttp.ClientSession()
        self.unsplash_token = self.bot.unsplash_token


    def get_online_users (self, member_list):

        online = []

        for u in member_list:
            if u.status == discord.Status.online and u.bot == False:
                online.append(u)

        return online



    @commands.command(name = 'random', aliases = ['rng', 'lucky'])
    @commands.guild_only()
    async def random (self, ctx, *args):

        """Returns a random value.
        This command accepts two options. You can use either one of them:
        user: Returns a randomly selected user that's currently online.
        choice: Takes a list of options and chooses a random option."""

        if not args:
            await ctx.send("This command accepts two options. You can use either one of them:\n"
                           "user: Returns a randomly selected user that's currently online.\n"
                           "choice: Takes a list of options and chooses a random option.")

        elif args[0] == 'user':
            online_users = self.get_online_users(ctx.guild.members)
            random_user  = random.choice(online_users)

            if ctx.channel.permissions_for(ctx.author).mention_everyone:
                winner = random_user.mention

            else:
                winner = random_user.display_name

            await ctx.send(f"And the winner is {winner}!")

        elif args[0] == 'choice':
            choices = list(args)
            choices.pop(0) # remove the "choice" keyword
            winner = random.choice(choices)
            await ctx.send(f"The winning option is {winner}.")



    @commands.command(name = 'cat', aliases = ['meow', 'randomcat'])
    async def get_random_cat (self, ctx):

        """Returns a random cat image."""

        try:
            async with self.session.get('http://aws.random.cat/meow') as response:
                parsed_response = await response.json()
                msg = await ctx.send (parsed_response['file'])
                await msg.add_reaction('🐾')

        except:
            await ctx.send("There are no cats around right now. 🐾")



    @commands.command(name = 'dog', aliases = ['woof', 'randomdog'])
    async def get_random_dog (self, ctx):

        """Returns a random dog image."""

        try:
            async with self.session.get('http://random.dog/woof') as response:
                filename = await response.text()
                msg = await ctx.send(f"https://random.dog/{filename}")
                await msg.add_reaction('🐶')

        except:
            await ctx.send("There are no dogs around right now. 🐶")



    @commands.command(name = 'fox', aliases = ['fox-noises', 'randomfox'])
    async def get_random_fox (self, ctx):

        """Returns a random fox image."""

        try:
            async with self.session.get('http://randomfox.ca/floof') as response:
                parsed_response = await response.json()
                msg = await ctx.send(parsed_response['image'])
                await msg.add_reaction('🦊')

        except:
            await ctx.send("There are no foxes around right now. 🦊")



    @commands.command(name = 'bunny', aliases = ['rabbit', 'chungus'])
    async def get_random_bunny (self, ctx):

        """Returns a random bunny image."""

        try:
            async with self.session.get(f'https://api.unsplash.com/search/photos?query=bunny&page={random.randint(0,10)}&per_page=30&client_id={self.unsplash_token}') as response:
                parsed_response = await response.json()
                entry_number    = random.randint(0,29)
                msg = await ctx.send(parsed_response['results'][entry_number]['links']['html'] + '?utm_source=unseen;ninja_bot&utm_medium=referral')
                await msg.add_reaction('🐰')

        except:
            await ctx.send("There are no bunnies around right now. 🐰")






def setup (bot):
    bot.add_cog(Fun(bot))
