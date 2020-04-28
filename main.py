import os
import aiohttp
import asyncio
import discord
import datetime
import configparser

from discord.ext import commands



class Ninja (commands.AutoShardedBot):

    def __init__ (self):

        config = configparser.ConfigParser()
        config.read('./config.ini')

        self.access_token   = config['tokens']['discord']
        self.command_prefix = config['bot']['prefix']
        self.home_guild     = int(config['bot']['home_guild'])
        self.log_channel    = int(config['bot']['log_channel'])
        self.description    = config['bot']['description']
        self.unsplash_token = config['tokens']['unsplash']

        self.session        = aiohttp.ClientSession()
        self.ready          = False



        super().__init__(command_prefix = self.command_prefix, description = self.description,
                         pm_help = None, help_attrs = dict(hidden = True),
                         fetch_offline_members = False, heartbeat_timeout = 150.0)



    async def on_connect (self):


        print('\n+---+---+---+---+---+---+---+---+---+---+---+---+')
        print('| u | n | s | e | e | n | \033[91m;\033[0m | n | i | n | j | a |')
        print('+---+---+---+---+---+---+---+---+---+---+---+---+\n')


        extensions = os.listdir('./cogs')
        for extension in extensions:

            if extension.endswith('.py'):
                extension_name = extension[:-3]

                try:
                    self.load_extension(f'cogs.{extension_name}')
                    print(f"Successfully loaded extension \033[94m{extension_name}\033[0m.")

                except:
                    print(f"Failed to load extension \033[94m{extension_name}\033[0m..")



    async def on_ready (self):

        if not self.ready:
            self.ready = True
            await self.change_presence(
                status   = discord.Status.online,
                activity = discord.Activity(
                    type = discord.ActivityType.listening,
                    name = f'{self.command_prefix}help'
                )
            )

        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f"\nLogged in as: \033[92m{self.user.name}\033[0m. (ID: {self.user.id})\n")



    async def on_command_error (self, ctx, error):

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send("This command cannot be used in private messages.")

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry. This command has been disabled.")

        elif isinstance(error, commands.MissingRequiredArgument):
            missing_argument = str(error).split(' ', 1)[0]
            await ctx.send(f"You're missing the following argument: `{missing_argument}`")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You're missing permissions to use this command.")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("The provided argument doesn't match the requirements.")

        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)



    async def process_commands (self, message):

        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        try:
            await self.invoke(ctx)
            print(f"[{datetime.datetime.now().strftime('%Y%m%d][%H:%M:%S')}] \033[92m{ctx.author}\033[0m issued command \033[94m{ctx.command}\033[0m.")

        except:
            print(f"Something went wrong while executing {ctx.command}")



    async def on_message (self, message):

        if message.author.bot:
            return

        await self.process_commands(message)



    def run (self):

        try:
            super().run(self.access_token, reconnect = True)

        except:
            print("Something went wrong while starting the bot.")
