import logging
import os

from dotenv import load_dotenv

from discord.ext import commands

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = commands.Bot(command_prefix='$')


modules = ["search"]

for module in modules:
    bot.load_extension("modules." + module)


bot.run(os.getenv("DISCORD_TOKEN"))
