import dbl
import discord
from discord.ext import commands
import json

with open("secrets.json") as json_file:
    secrets = json.load(json_file)

class topgg(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = secrets["topgg_key"]
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

def setup(bot):
    bot.add_cog(topgg(bot))
