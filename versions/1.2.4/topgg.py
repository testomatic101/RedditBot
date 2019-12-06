import dbl
import discord
from discord.ext import commands


class topgg(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                     ".eyJpZCI6IjQzNzQzOTU2MjM4NjUwNTczMCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTc1NTc2MTU1fQ" \
                     ".LbuHaiap7xTKvytdqGnkSpgISUp8cbOzyJ4BETm2eYg "
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

    async def on_guild_post(self, ctx):
        await ctx.change_presence(status=discord.Status.do_not_disturb,
                                  activity=discord.Game(name="!help | In " + str(len(ctx.guilds)) + " servers"))
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(topgg(bot))