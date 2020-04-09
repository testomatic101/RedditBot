from discord.ext import commands
import discord
import praw
import json
import random
import os
from pathlib import Path

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True

# login to reddit
reddit = praw.Reddit(client_id="ivBqfmemZfkbCg",
                     client_secret="FoCd7bYKppGz2gsAX8cVNHJ9Vy4",
                     user_agent='redditbot created by bwac#2517')
# make the bot client
bot = commands.Bot(command_prefix='r')

# this is used for the footer of embeds
version = '1.3.1 https://rbdis.xyz/ redditbot created by bwac#2517'
# red for embeds
red = 0xFF0000

# remove the help so we can have a custom one
bot.remove_command('help')

# all the cogs
extensions = ["user", "subreddit", "utils"]
if production:
    extensions.append("topgg")


@bot.event
async def on_ready():
    # make the presence when the bot is ready
    print('ready')
    print(bot.guilds)
    for guild in bot.guilds:
        sent = False
        for invite in await guild.invites():
            if not sent:
                print(invite)
                sent = True
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="rhelp | In " + str(len(bot.guilds)) + " servers"))


@bot.event
async def on_command_completion(ctx):
    if random.randint(1, 2) == 1:
        votemessage = discord.Embed(title="Hey! We are doing a giveaway in our server!",
                                  description="If you didnt know we have a server, come join (and maybe score nitro one day) :D https://rbdis.xyz/server",
                                  color=red)
        await ctx.send(embed=votemessage)
    else:
        feedbackmessage = discord.Embed(title="Have you found a bug?",
                                    description="report it here http://rbdis.xyz/bugreport",
                                    color=red)
        await ctx.send(embed=feedbackmessage)

if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    if production:
        bot.run("NDM3NDM5NTYyMzg2NTA1NzMw.Xo-rqg.FqejXDalSyWb6liRlIM0zIh3DR8")
    else:
        bot.run("NjUwNTgzNzk5MDQxNjIyMDQ2.Xo-p5Q.Yqay6C0bnzY0pxYvE4ZLhZ6gfmU")
