import random
import aiohttp
import discord

from discord.ext import commands



class Fun (commands.Cog):


    def __init__ (self, bot):

        self.bot            = bot
        self.session        = self.bot.session
        self.unsplash_token = self.bot.unsplash_token


    def get_online_users (self, member_list):

        online = []

        for u in member_list:
            if u.status == discord.Status.online and u.bot == False:
                online.append(u)

        return online



    @commands.group(name = 'random', aliases = ['rng', 'lucky'])
    async def random (self, ctx):

        """Returns something random."""

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
                e = discord.Embed()
                e.set_image(url = parsed_response['results'][entry_number]['urls']['regular'])
                e.set_footer(text = 'Photographer: ' + parsed_response['results'][entry_number]['user']['name'])
                e.add_field(name = 'Link', value = parsed_response['results'][entry_number]['user']['links']['html'] + '?utm_source=unseen;ninja_bot&utm_medium=referral')
                msg = await ctx.send(embed = e)
                await msg.add_reaction('🐰')

        except:
            await ctx.send("There are no bunnies around right now. 🐰")



    @commands.group(name = 'meme')
    async def _meme (self, ctx):

        """Create your own memes!"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @_meme.command(name = 'create', aliases = ['make'])
    async def create_meme (self, ctx, template: str, line1: str, line2: str):

        """Example: ;meme create snek \"No booper\" \"do NOT!\""""

        def escape_literals (content):
            return content.replace('-', '--').replace('_', '__').replace('?', '~q').replace(' ', '%20').replace("''", "\"")

        try:
            async with self.session.get(f'https://memegen.link/{template}/{escape_literals(line1)}/{escape_literals(line2)}') as response:
                parsed_response = await response.json()
                image_link = parsed_response['direct']['masked']
                await ctx.send(image_link)

        except Exception as e:
            await ctx.send(e)



    @_meme.command(name = 'templates', aliases = ['list'])
    async def list_templates (self, ctx):

        """See available templates."""

        await ctx.send('See a list of available templates here: https://memegen.link/api/templates/')






def setup (bot):
    bot.add_cog(Fun(bot))
