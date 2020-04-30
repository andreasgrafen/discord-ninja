import re
import discord

from utils       import http
from discord.ext import commands



class Reactions (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot


    def has_exact_match (self, triggers, message):

        values = []

        for item in triggers:
            if re.search(r'\b' + item + r'\b', message):
                values.append(True)

            else:
                values.append(False)

        return values



    @commands.Cog.listener()
    async def on_message (self, ctx):

        if ctx.clean_content.startswith(self.bot.command_prefix) or ctx.author.bot:
            return

        # :lollipop:
        if re.search(r'\bloli\b', ctx.clean_content.lower()):
            await ctx.add_reaction('🍭')

        # :eggplant:
        eggplant_triggers = ['penis', 'cock', 'cocks', 'dick', 'dicks']
        if any(self.has_exact_match(eggplant_triggers, ctx.clean_content.lower())) is True:
            msg = await ctx.channel.send('I have the biggest one around here.')
            await msg.add_reaction('🍆')

        # :duck:
        duck_triggers = ['duck', 'ducks', 'quack', 'dick', 'dicks']
        if any(self.has_exact_match(duck_triggers, ctx.clean_content.lower())) is True:
            await ctx.add_reaction('🦆')

        # :poop:
        poop_triggers = ['poop', 'shit', 'bullshit']
        if any(self.has_exact_match(poop_triggers, ctx.clean_content.lower())) is True:
            await ctx.add_reaction('💩')

        # :heart:
        heart_triggers = ['heart', 'love', '<3']
        if any(self.has_exact_match(heart_triggers, ctx.clean_content.lower())) is True:
            await ctx.add_reaction('❤')

        # :gay:
        gay_triggers = ['gay', 'gae', 'homo']
        if any(self.has_exact_match(gay_triggers, ctx.clean_content.lower())) is True:
            hearts = ['❤', '🧡', '💛', '💚', '💙', '💜']
            for heart in hearts:
                await ctx.add_reaction(heart)

        # :peach:
        peach_triggers = ['butt', 'butts', 'ass', 'peach', 'peaches']
        if any(self.has_exact_match(peach_triggers, ctx.clean_content.lower())) is True:
            await ctx.add_reaction('🍑')



    @commands.command(name = 'hug')
    async def hug_reaction (self, ctx, *, member: discord.Member = None):

        hug_gif = ''

        if not member:
            member = ctx.author

        try:
            response = await http.get('https://some-random-api.ml/animu/hug', res_method = 'json')
            hug_gif = response['link']

        except:
            pass

        await ctx.send(f"{ctx.author.mention} hugs {member.mention}\n{hug_gif}")



    @commands.command(name = 'pat')
    async def pat_reaction (self, ctx, *, member: discord.Member = None):

        pat_gif = ''

        if not member:
            member = ctx.author

        try:
            response = await http.get('https://some-random-api.ml/animu/pat', res_method = 'json')
            pat_gif = response['link']

        except:
            pass

        await ctx.send(f"{ctx.author.mention} pats {member.mention}\n{pat_gif}")



    @commands.command(name = 'wink')
    async def wink_reaction (self, ctx, *, member: discord.Member = None):

        wink_gif = ''

        if not member:
            member = ctx.author

        try:
            response = await http.get('https://some-random-api.ml/animu/wink', res_method = 'json')
            wink_gif = response['link']

        except:
            pass

        await ctx.send(f"{ctx.author.mention} winks at {member.mention}\n{wink_gif}")





def setup (bot):
    bot.add_cog(Reactions(bot))
