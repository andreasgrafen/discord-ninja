import discord

from discord.ext import commands



class Admin (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.command(hidden = True, name = 'load')
    @commands.is_owner()
    async def load_cog (self, ctx, *, extension: str):

        msg = await ctx.send(f"Attempting to load {extension}.")

        try:
            self.bot.load_extension(f'cogs.{extension}')
            await msg.edit(content = f"Successfully loaded {extension}.")

        except:
            await msg.edit(content = f"There was an error loading {extension}.")



    @commands.command(hidden = True, name = 'unload')
    @commands.is_owner()
    async def unload_cog (self, ctx, *, extension: str):

        msg = await ctx.send(f"Attempting to unload {extension}.")

        if f'cogs.{extension}' in self.bot.extensions:

            try:
                self.bot.unload_extension(f'cogs.{extension}')
                await msg.edit(content = f"Successfully unloaded {extension}.")

            except:
                await msg.edit(content = f"There was an error unloading {extension}.")

        else:
            await msg.edit(content = f"This extension ({extension}) doesn't exist.")



    @commands.command(hidden = True, name = 'reload')
    @commands.is_owner()
    async def reload_cog (self, ctx, *, extension: str):

        msg = await ctx.send(f"Attempting to reload {extension} ...")

        if f'cogs.{extension}' in self.bot.extensions:

            try:
                self.bot.unload_extension(f'cogs.{extension}')
                self.bot.load_extension(f'cogs.{extension}')
                await msg.edit(content = f"Successfully reloaded {extension}.")

            except:
                await msg.edit(content = f"There was an error reloading {extension}.")

        else:
            await msg.edit(content = f"This extension ({extension}) doesn't exist.")





def setup (bot):
    bot.add_cog(Admin(bot))
