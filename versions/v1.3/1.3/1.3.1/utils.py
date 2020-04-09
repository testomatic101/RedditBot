import discord
from discord.ext import commands
import praw
import datetime
import json
from sys import platform

version = '1.3.1 Created by bwac#2517'
red = 0xFF0000

# topggclient = dbl.DBLClient(bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzNzQzOTU2MjM4NjUwNTczMCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTg1ODA5MDQ2fQ.5IZ449Tf5mj5ZEaXORVKuZ2SKL6KcaySkgE8unc59-4")

class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='help')
    async def newhelp(self, ctx):
        # custom help command
        # make the embeds
        helpembed = discord.Embed(title="**http://rbdis.xyz**",
                             description="help",
                             color=red)
        # botinfo = await topggclient.get_bot_info()
        # getto = botinfo.get('monthlyPoints') + 10
        # helpembed.add_field(name="\n\nThe bot currently has **" + str(botinfo.get('monthlyPoints')) + "** votes, can we get it to **" + str(getto) + "**?", value='https://top.gg/bot/437439562386505730/vote', inline=False)
        helpembed.add_field(name="Join the server!", value="http://rbdis.xyz/server/", inline=False)
        helpembed.add_field(name="Found a bug?", value="Report it here http://rbdis.xyz/bugreport/", inline=False)
        helpembed.add_field(name="Please give your feedback!", value="http://rbdis.xyz/feedback", inline=False)

        commandsembed = discord.Embed(title="Help:",
                             description="**Commands**",
                             color=red)
        commandsembed.add_field(name="rhelp", value="Shows this page", inline=False)
        commandsembed.add_field(name="rr [sub name here]", value="Gives you some info on a subreddit", inline=False)
        commandsembed.add_field(name="ru [username here]", value="Gives you some info on a user", inline=False)
        commandsembed.add_field(name="rforce [sub name here]", value="Removes subreddit cache", inline=False)
        await ctx.author.send(embed=helpembed)
        await ctx.author.send(embed=commandsembed)

    # update status
    @commands.command()
    async def update(ctx):
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="rhelp | In " + str(len(bot.guilds)) + " servers"))

def setup(bot):
    bot.add_cog(utils(bot))
