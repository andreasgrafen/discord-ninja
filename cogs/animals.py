import random
import discord

from utils import http
from discord.ext import commands



class Animals (commands.Cog):


    def __init__ (self, bot):

        self.bot            = bot
        self.unsplash_token = self.bot.unsplash_token



    @commands.command(name = 'cat', aliases = ['meow', 'randomcat'])
    async def get_random_cat (self, ctx):

        """Returns a random cat image."""

        async with ctx.channel.typing():

            try:
                response = await http.get('http://aws.random.cat/meow', res_method = 'json')
                msg = await ctx.send (response['file'])
                await msg.add_reaction('🐾')

            except:
                await ctx.send("There are no cats around right now. 🐾")



    @commands.command(name = 'dog', aliases = ['woof', 'randomdog'])
    async def get_random_dog (self, ctx):

        """Returns a random dog image."""

        async with ctx.channel.typing():

            try:
                response = await http.get('http://random.dog/woof', res_method = 'text')
                msg = await ctx.send(f"https://random.dog/{response}")
                await msg.add_reaction('🐶')

            except:
                await ctx.send("There are no dogs around right now. 🐶")



    @commands.command(name = 'fox', aliases = ['fox-noises', 'randomfox'])
    async def get_random_fox (self, ctx):

        """Returns a random fox image."""

        async with ctx.channel.typing():

            try:
                response = await http.get('http://randomfox.ca/floof', res_method = 'json')
                msg = await ctx.send(response['image'])
                await msg.add_reaction('🦊')

            except:
                await ctx.send("There are no foxes around right now. 🦊")



    @commands.command(name = 'bunny', aliases = ['rabbit', 'chungus'])
    async def get_random_bunny (self, ctx):

        """Returns a random bunny image."""

        async with ctx.channel.typing():

            try:
                r = random.randint(0,10)
                t = self.unsplash_token
                url = f'https://api.unsplash.com/search/photos?query=bunny&page={r}&per_page=30&client_id={t}'

                response = await http.get(url, res_method = 'json')
                entry_number = random.randint(0,29)

                e = discord.Embed()
                e.set_image(url = response['results'][entry_number]['urls']['regular'])
                e.set_footer(text = 'Photographer: ' + response['results'][entry_number]['user']['name'])
                e.add_field(name = 'Link', value = response['results'][entry_number]['user']['links']['html'] + '?utm_source=unseen;ninja_bot&utm_medium=referral')

                msg = await ctx.send(embed = e)
                await msg.add_reaction('🐰')

            except:
                await ctx.send("There are no bunnies around right now. 🐰")





def setup (bot):
    bot.add_cog(Animals(bot))
