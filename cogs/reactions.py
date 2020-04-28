import discord

from discord.ext import commands



class Reactions (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_message (self, ctx):

        if ctx.clean_content.startswith(self.bot.command_prefix) or ctx.author.bot:
            return

        # :lollipop:
        if 'loli' in ctx.clean_content.lower():
            await ctx.add_reaction('🍭')

        # :eggplant:
        eggplant_triggers = ['penis', 'cock', 'dick']
        if any(item in ctx.clean_content.lower() for item in eggplant_triggers):
            msg = await ctx.channel.send('I have the biggest one around here.')
            await msg.add_reaction('🍆')

        # :duck:
        duck_trigger = ['duck', 'quack', 'dick']
        if any(item in ctx.clean_content.lower() for item in duck_trigger):
            await ctx.add_reaction('🦆')

        # :poop:
        poop_trigger = ['poop', 'shit']
        if any(item in ctx.clean_content.lower() for item in poop_trigger):
            await ctx.add_reaction('💩')

        # :heart:
        heart_trigger = ['heart', 'love', '<3']
        if any(item in ctx.clean_content.lower() for item in heart_trigger):
            await ctx.add_reaction('❤')

        # :gay:
        gay_trigger = ['gay', 'gae', 'homo']
        if any(item in ctx.clean_content.lower() for item in gay_trigger):
            hearts = ['❤', '🧡', '💛', '💚', '💙', '💜']
            for heart in hearts:
                await ctx.add_reaction(heart)

        # :peach:
        peach_trigger = ['butt', 'ass', 'peach']
        if any(item in ctx.clean_content.lower() for item in peach_trigger):
            await ctx.add_reaction('🍑')





def setup (bot):
    bot.add_cog(Reactions(bot))
