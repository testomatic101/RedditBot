import discord
from discord.ext import commands
import json, os

version_number = "1.4.2"
version = version_number + " Created by bwac#2517"
red = 0xFF0000

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True

with open("secrets.json") as json_file:
    secrets = json.load(json_file)


class utils(commands.Cog):
    """help, about, invite ect is here"""

    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ""

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        about = discord.Embed(
            title="About",
            description="Hey, im RedditBot!\nIm made by bwac#2517\nIm currently running version "
            + version_number
            + "\nIm in "
            + str(len(self.bot.guilds))
            + " servers"
            + "\nMy site is https://rbdis.xyz\nIm made using discord.py\nMy github is https://github.com/BWACpro/RedditBot",
            color=red,
        )
        await ctx.send(embed=about)

    # clear cache/temp files (only for bwac)
    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx, what_to_clear=None):
        dir = ""
        if what_to_clear == "temp":
            dir = "temp"
        elif what_to_clear == "subreddits":
            dir = "cache/subreddits"
        elif what_to_clear == "users":
            dir = "cache/users"
        filelist = [f for f in os.listdir(dir)]
        for f in filelist:
            os.remove(os.path.join(dir, f))
            await ctx.send("deleted " + f)
        await ctx.send("tried my best")


def setup(bot):
    bot.add_cog(utils(bot))
