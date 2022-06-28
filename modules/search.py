import os

import async_cse
import discord
from discord.ext import commands
from dotenv import load_dotenv

from image_search.searcher import Searcher


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.searcher = Searcher(os.getenv("CSE_TOKENS").split("\n"))

    @commands.command()
    async def search_image(self, ctx, *, query: str):
        try:
            image_extension, image_bytes = await self.searcher.search_get_image(query)
            image_file = discord.File(fp=image_bytes, filename=f"image.{image_extension}")
            await ctx.send(file=image_file)
        except async_cse.search.NoResults:
            await ctx.send("Ничего не нашлось ;(")


def setup(bot):
    bot.add_cog(Search(bot))
