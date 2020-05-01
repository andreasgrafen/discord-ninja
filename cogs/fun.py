import random
import discord
import datetime
import textwrap

from discord     import File
from discord.ext import commands
from utils       import http

from PIL         import Image
from PIL         import ImageFont
from PIL         import ImageDraw



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
    async def create_meme (self, ctx, top_text: str, bottom_text: str):

        """Example: ;meme create \"No booper\" \"do NOT!\""""

        try:
            await ctx.message.attachments[0].save('images/input.png')

        except:
            await ctx.send('Please also send me an image.')
            return


        with ctx.channel.typing():

            try:

                image                   = Image.open('images/input.png')
                watermark               = Image.open('images/watermark.png')
                draw                    = ImageDraw.Draw(image)
                img_width, img_height   = image.size
                font_size               = (img_height//10) if (img_height <= img_width) else (img_width//10)
                font                    = ImageFont.truetype('./assets/font.otf', font_size)
                char_width, char_height = font.getsize('A')
                line_length             = img_width//char_width
                top_lines               = textwrap.wrap(top_text, width = line_length)
                bottom_lines            = textwrap.wrap(bottom_text, width = line_length)
                top_text_concat         = '\n'.join(top_lines)
                bottom_text_concat      = '\n'.join(bottom_lines)

                top_text_width, top_text_height = draw.multiline_textsize(top_text_concat, font = font, spacing = 10)
                draw.multiline_text(((img_width-top_text_width)/2, 10), top_text_concat, font = font, spacing = 10, align = 'center')

                bottom_text_width, bottom_text_height = draw.multiline_textsize(bottom_text_concat, font = font, spacing = 10)
                draw.multiline_text(((img_width-bottom_text_width)/2, (img_height-bottom_text_height)-20), bottom_text_concat, font = font, spacing = 10, align = 'center')

                watermark_size = font_size
                watermark = watermark.resize((watermark_size, watermark_size))

                canvas = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
                canvas.paste(image, (0, 0))
                canvas.paste(watermark, (0, img_height-font_size), mask = watermark)
                canvas.save('images/output.png', 'PNG')

                await ctx.channel.purge(limit = 1) # remove the message invoking this command
                await ctx.send(content = f"Here is your meme {ctx.author.mention}.", file = File('images/output.png'))

            except Exception as e:
                await ctx.send(e)



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

        """Get instructions for a specified cocktail."""

        async with ctx.channel.typing():

            e = await self.get_cocktail_info(cocktail_id)
            await ctx.send(embed = e)



    @cocktail.command(name = 'random', aliases = ['r'])
    async def get_random_cocktail (self, ctx):

        """Get a completely random cocktail revipe."""

        async with ctx.channel.typing():

            try:
                response = await http.get(f'https://www.thecocktaildb.com/api/json/v1/1/random.php', res_method = 'json')
                cocktail_id = response['drinks'][0]['idDrink']

            except Exception as e:
                await ctx.send(e)

            e = await self.get_cocktail_info(cocktail_id)
            await ctx.send(embed = e)



    @commands.command(name = 'amazon', aliases = ['review'])
    async def fake_review (self, ctx, rating: int = 5, rating_text: str = 'Best product ever!', *, content: str = 'ICH MAG ES!'):

        avatar = ctx.author.avatar_url_as(static_format = 'png')
        await avatar.save('images/avatar.png')

        try:

            font_regular = ImageFont.truetype('./assets/review.ttf', 13)
            font_bold    = ImageFont.truetype('./assets/review-bold.ttf', 13)
            font_small   = ImageFont.truetype('./assets/review-bold.ttf', 11)

            # get body content size
            review_body_size = Image.new('RGBA', (760, 1000), (0, 0, 0, 0))
            review_draw      = ImageDraw.Draw(review_body_size)

            char_width, char_height = font_regular.getsize('M')
            line_length             = 1000/char_width
            content_lines           = textwrap.wrap(content, width = line_length)
            body_copy               = '\n'.join(content_lines)

            content_width, content_height = review_draw.multiline_textsize(body_copy, font = font_regular, spacing = 6)


            review     = Image.new('RGBA', (700, content_height + 170), '#FFFFFF')
            user_image = Image.open('images/avatar.png')
            user_mask  = Image.open('images/avatar-mask.png')
            stars      = Image.open(f'images/stars-{rating}.png')

            draw = ImageDraw.Draw(review)

            # get text boundaries
            user_name_w, user_name_h     = draw.textsize(ctx.author.display_name, font = font_regular)
            rating_text_w, rating_text_h = draw.textsize(rating_text, font = font_bold)

            # resize assets
            user_image  = user_image.resize((34, 34))
            stars       = stars.resize((90, 18))

            # place assets
            review.paste(user_image, (20, 20), mask = user_mask)
            review.paste(stars, (20, 64))

            # place text
            draw.text((64, ((34-user_name_h)/2)+20), ctx.author.display_name, '#111111', font = font_regular)
            draw.text((120, (82-rating_text_h)), rating_text, '#111111', font = font_bold)
            draw.text((20, 85), f"Reviewed as a Meme on {datetime.datetime.now().strftime('%B %d, %Y')}.", '#555555', font = font_regular)
            draw.text((20, 105), 'Verified Purchase', '#C45500', font = font_small)
            draw.multiline_text((20, 130), body_copy, '#111111', font = font_regular, spacing = 6)
            draw.text((20, content_height + 140), f"{random.randint(1, 200)} people found this helpful.", '#767676', font = font_regular)

            # save and send
            review.save('images/amazon.png', 'PNG')
            await ctx.send(file = File('images/amazon.png'))

        except Exception as e:
            await ctx.send(e)





def setup (bot):
    bot.add_cog(Fun(bot))
