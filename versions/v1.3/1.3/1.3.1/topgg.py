import dbl
import discord
from discord.ext import commands
import json

class topgg(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzNzQzOTU2MjM4NjUwNTczMCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTg1ODA5MDQ2fQ.5IZ449Tf5mj5ZEaXORVKuZ2SKL6KcaySkgE8unc59-4"
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post(self, ctx):
        await bot.change_presence(status=discord.Status.do_not_disturb,
                                  activity=discord.Game(name="rhelp | In " + str(len(ctx.guilds)) + " servers"))
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(topgg(bot))
