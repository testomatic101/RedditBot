import dbl
import discord
from discord.ext import commands
import json

secrets = None
with open('C:/Users/Noahd/Documents/secrets.json') as json_file:
    secrets = json.load(json_file)

class topgg(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = secrets["top.gg"]["token"]
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post(self, ctx):
        await ctx.change_presence(status=discord.Status.do_not_disturb,
                                  activity=discord.Game(name="rhelp | In " + str(len(ctx.guilds)) + " servers"))
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(topgg(bot))
