import asyncio
from itertools import cycle
import os

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands, tasks
from tools.autocogs import AutoCogs
from dotenv import load_dotenv
import threading
from pycord_components import PycordComponents
import config
load_dotenv(verbose=True)
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        AutoCogs(self)
        self.remove_command("help")
    async def on_ready(self):
        """Called upon the READY event"""
        await self.change_presence(status=discord.Status.online, activity=discord.Activity(name="짱구야 도움",
                                                                                               type=discord.ActivityType.playing))
        print("Bot is ready.")
    async def is_owner(self, user):
        if user.id in config.OWNER:
            return True
    @staticmethod
    async def create_db_con():
        db = await aiosqlite.connect("db/db.sqlite")
        MyBot.db = discordSuperUtils.DatabaseManager.connect(database=db)




INTENTS = discord.Intents.all()
my_bot = MyBot(command_prefix=["짱구야 ","짱구야","ㄱ","ㄱ "], intents=INTENTS)


PycordComponents(my_bot)
if __name__ == "__main__":
    my_bot.loop.run_until_complete(MyBot.create_db_con())
    my_bot.run(os.getenv('TOKEN'))