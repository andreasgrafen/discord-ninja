import random
import aiohttp
import discord

from discord.ext import commands



class Animals (commands.Cog):


    def __init__ (self, bot):

        self.bot            = bot
        self.session        = self.bot.session
        self.unsplash_token = self.bot.unsplash_token



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





def setup (bot):
    bot.add_cog(Animals(bot))
