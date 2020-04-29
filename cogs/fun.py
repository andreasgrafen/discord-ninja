import random
import discord

from utils import http
from discord.ext import commands



class Fun (commands.Cog):


    def __init__ (self, bot):

        self.bot            = bot
        self.session        = self.bot.session



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

        async with ctx.channel.typing():

            try:
                response = await http.get(f'https://memegen.link/{template}/{escape_literals(line1)}/{escape_literals(line2)}', res_method = 'json')
                await ctx.send(response['direct']['masked'])

            except Exception as e:
                await ctx.send(e)



    @_meme.command(name = 'templates', aliases = ['list'])
    async def list_templates (self, ctx):

        """See available templates."""

        await ctx.send('See a list of available templates here: https://memegen.link/api/templates/')



    @commands.group(name = 'cocktail', aliases = ['cocktails'])
    async def cocktail (self, ctx):

        """All the cocktail things!"""

        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))



    @cocktail.command(name = 'search', aliases = ['find', 'grab'])
    async def search_cocktails (self, ctx, *, cocktailname: str):

        """Search for cocktails by name."""

        async with ctx.channel.typing():

            try:
                response = await http.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktailname}', res_method = 'json')
                cocktail_list = '**Cocktail Results:**\n'

                try:
                    for cocktail in response['drinks']:
                        cocktail_list += f"{cocktail['strDrink']}: `{cocktail['idDrink']}`\n"
                    await ctx.send(cocktail_list)

                except:
                    await ctx.send("I couldn't find any cocktails for that searchterm. :c")

            except Exception as e:
                await ctx.send(e)



    async def get_cocktail_info (self, cocktail_id):

        try:
            response = await http.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}', res_method = 'json')

            if response['drinks'] is None:
                f = discord.Embed()
                f.add_field(name = 'error', value = f'There is no cocktail with this ID.\nSearch for a drink with `{self.bot.command_prefix}cocktail search`.')
                return f

            cocktail = response['drinks'][0]

            ingredients = ''
            index = 1
            while index <= 15:
                ingredient = f"{cocktail[f'strIngredient{index}']}"
                amount     = f"{cocktail[f'strMeasure{index}']}"
                if cocktail[f'strIngredient{index}'] is not None:
                    if cocktail[f'strMeasure{index}'] is None:
                        ingredients += f"{ingredient}\n"
                    else:
                        ingredients += f"{amount}of {ingredient}\n"
                index += 1

            e = discord.Embed(title = f"{cocktail['strDrink']} ({cocktail['strAlcoholic']})")
            e.add_field(name = 'Ingredients', value = ingredients)
            e.add_field(name = 'Instructions', value = cocktail[f'strInstructions'])
            e.set_thumbnail(url = cocktail['strDrinkThumb'])

            return e

        except Exception as e:
            return e



    @cocktail.command(name = 'get', aliases = ['recipe', 'info'])
    async def get_cocktail (self, ctx, cocktail_id: int):

        async with ctx.channel.typing():

            e = await self.get_cocktail_info(cocktail_id)
            await ctx.send(embed = e)



    @cocktail.command(name = 'random', aliases = ['r'])
    async def get_random_cocktail (self, ctx):

        async with ctx.channel.typing():

            try:
                response = await http.get(f'https://www.thecocktaildb.com/api/json/v1/1/random.php', res_method = 'json')
                cocktail_id = response['drinks'][0]['idDrink']

            except Exception as e:
                await ctx.send(e)

            e = await self.get_cocktail_info(cocktail_id)
            await ctx.send(embed = e)





def setup (bot):
    bot.add_cog(Fun(bot))
