import re
import discord

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





def setup (bot):
    bot.add_cog(Reactions(bot))
