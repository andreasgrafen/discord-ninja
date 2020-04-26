import discord

from discord.ext import commands



class Admin (commands.Cog):


    def __init__ (self, bot):

        self.bot = bot



    @commands.command(hidden = True, name = 'shutdown')
    @commands.is_owner()
    async def shutdown_bot (self, ctx):

        await ctx.send("Shutting down the bot.")
        await self.bot.session.close()
        await self.bot.logout()
        await self.bot.close()



    @commands.command(hidden = True, name = 'status')
    @commands.is_owner()
    async def change_status (self, ctx, type, *, content):

        if type == 'play':
            status_type = discord.ActivityType.playing

        elif type == 'listen':
            status_type = discord.ActivityType.listening

        elif type == 'watch':
            status_type = discord.ActivityType.watching

        else:
            await ctx.send("Please specify a viable activity type. Available options are: `play`, `listen` and `watch`.")
            return

        try:
            await self.bot.change_presence(
                activity = discord.Activity(
                    type = status_type,
                    name = content
                )
            )

        except:
            await ctx.send("Something went wrong while changing the bots status.")



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
