from discord.ext import commands
import discord
import praw
import dbl
import json
import random
from pathlib import Path


# login to reddit
reddit = praw.Reddit(client_id="ivBqfmemZfkbCg",
                     client_secret="FoCd7bYKppGz2gsAX8cVNHJ9Vy4",
                     user_agent='redditbot created by bwac#2517')
# make the bot client
bot = commands.Bot(command_prefix='r')

# this is used for the footer of embeds
version = '1.2.5 https://rbdis.xyz redditbot created by bwac#2517'
# red for embeds
red = 0xFF0000

# make the top.gg api client
topggclient = dbl.DBLClient(bot, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQzNzQzOTU2MjM4NjUwNTczMCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTg1ODA5MDQ2fQ.5IZ449Tf5mj5ZEaXORVKuZ2SKL6KcaySkgE8unc59-4")

# remove the help so we can have a custom one
bot.remove_command('help')


@commands.command(name='help')
async def newhelp(ctx):
    # custom help command
    # make the embeds
    helpembed = discord.Embed(title="**http://rbdis.xyz**",
                         description="help",
                         color=red)
    botinfo = await topggclient.get_bot_info()
    getto = botinfo.get('monthlyPoints') + 10
    helpembed.add_field(name="\n\nThe bot currently has **" + str(botinfo.get('monthlyPoints')) + "** votes, can we get it to **" + str(getto) + "**?", value='https://top.gg/bot/437439562386505730/vote', inline=False)
    helpembed.add_field(name="Found a bug?", value="Report it here http://rbdis.xyz/bugreport/", inline=False)
    helpembed.add_field(name="Please give your feedback!", value="http://rbdis.xyz/feedback", inline=False)

    commandsembed = discord.Embed(title="Help:",
                         description="**Commands**",
                         color=red)
    commandsembed.add_field(name="rhelp", value="Shows this page", inline=False)
    commandsembed.add_field(name="rr [sub name here]", value="Gives you some info on a subreddit", inline=False)
    commandsembed.add_field(name="ru [username here]", value="Gives you some info on a user", inline=False)
    # help_user = discord.Embed(title="User commands:",
    #                           description="**Commands to add accounts and account management**", color=red)
    # help_user.add_field(name="rconnect [user name here]", value="Connect a reddit connect", inline=False)
    # help_user.add_field(name="runconnect", value="Unconnect the reddit account that you have connected",
    #                     inline=False)
    # help_user.add_field(name="rcode", value="Submit the code you got from reddit", inline=False)
    # help_user.add_field(name="rme", value="See your account", inline=False)
    # help_user.set_footer(text="RedditBot " + version)
    await ctx.author.send(embed=helpembed)
    await ctx.author.send(embed=commandsembed)
# add the new help command
bot.add_command(newhelp)


# the feedback command is for users to send feedback
@commands.command()
async def feedback(ctx):
    await ctx.send("You can send feedback here http://rbdis.xyz/?page_id=474")
# add the feedback command
bot.add_command(feedback)

# update status
@commands.command()
async def update(ctx):
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="rhelp | In " + str(len(bot.guilds)) + " servers"))
bot.add_command(update)
    
# all the cogs
extensions = ["user", "subreddit", "topgg"]


@bot.event
async def on_ready():
    # make the presence when the bot is ready

    print('ready')
    print(bot.guilds)
    print(await topggclient.get_bot_upvotes())
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
        votemessage = discord.Embed(title="wanna help out the bot?",
                                  description="if you didnt know, top.gg resets all votes every month. So it would mean even more to me if you voted at https://top.gg/bot/437439562386505730/vote",
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
    bot.run("lV30ctXjGC56kAUxldKyfq7SDqB-GYVj")
