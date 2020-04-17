from discord.ext import commands
import discord
import praw
import json
import random
import dbl
import os

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True


with open("secrets.json") as json_file:
    secrets = json.load(json_file)

# this is used for the footer of embeds
version_number = "1.4"
version = version_number + "https://rbdis.xyz/ redditbot created by bwac#2517"
# red for embeds
red = 0xFF0000

# login to reddit
reddit = praw.Reddit(
    client_id=secrets["reddit_id"],
    client_secret=secrets["reddit_secret"],
    user_agent="discord:n/a:" + version_number + " (by /u/-_-BWAC-_-)",
)

# make the bot client
bot = commands.Bot(command_prefix="r!", help_command=None)

if production:
    # make the top.gg api client
    topggclient = dbl.DBLClient(bot, secrets["topgg_key"])


@commands.command(name="help")
async def newhelp(ctx):
    # custom help command
    # make the embeds
    helpembed = discord.Embed(
        title="**http://rbdis.xyz**", description="help", color=red
    )
    if production:
        botinfo = await topggclient.get_bot_info()
        getto = botinfo.get("monthlyPoints") + 10
        helpembed.add_field(
            name="\n\nThe bot currently has **"
            + str(botinfo.get("monthlyPoints"))
            + "** votes, can we get it to **"
            + str(getto)
            + "**?",
            value="https://top.gg/bot/437439562386505730/vote",
            inline=False,
        )
    helpembed.add_field(
        name="Join the server!", value="http://rbdis.xyz/server/", inline=False
    )
    helpembed.add_field(
        name="Found a bug?",
        value="Report it here http://rbdis.xyz/bugreport/",
        inline=False,
    )
    helpembed.add_field(
        name="Please give your feedback!",
        value="http://rbdis.xyz/feedback",
        inline=False,
    )

    commandsembed = discord.Embed(title="Help:", description="**Commands**", color=red)
    commandsembed.add_field(name="r!help", value="Shows this page", inline=False)
    commandsembed.add_field(
        name="r!subreddit [sub name here]",
        value="Gives you some info on a subreddit",
        inline=False,
    )
    commandsembed.add_field(
        name="r!user [username here]",
        value="Gives you some info on a user",
        inline=False,
    )
    commandsembed.add_field(
        name="r!resetsub [sub name here]", value="Removes subreddit cache", inline=False
    )
    commandsembed.add_field(
        name="r!resetuser [user name here]", value="Removes user cache", inline=False
    )
    commandsembed.add_field(
        name="r!hot [sub name here]", value="Shows the top 10 hot posts", inline=False
    )
    commandsembed.add_field(
        name="r!top [sub name here]", value="Shows the top 10 top posts", inline=False
    )

    await ctx.send(embed=helpembed)
    await ctx.send(embed=commandsembed)


# add the new help command
bot.add_command(newhelp)


# update status
@commands.command()
async def update(ctx):
    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Game(name="r!help | In " + str(len(bot.guilds)) + " servers"),
    )


# add the update command
bot.add_command(update)


@bot.event
async def on_command_error(ctx, error):
    """Sends error to user and channel"""
    await ctx.send(
        str(ctx.author)
        + ", something went wrong. \n`"
        + str(error)
        + "`\nIf it keeps happening report it here https://rbdis.xyz/bugreport or https://rbdis.xyz/server\nThank you!"
    )

    await bot.get_channel(700277796148215838).send(
        "Author: " + str(ctx.author) + "\nError:\n```" + str(error) + "```"
    )


@bot.event
async def on_command_completion(ctx):
    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Game(name="r!help | In " + str(len(bot.guilds)) + " servers"),
    )


# all the cogs
extensions = ["cogs.user", "cogs.subreddit"]
if production:
    extensions.append("cogs.topgg")


@bot.event
async def on_ready():
    """When the bot is ready."""
    print("ready>")


if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    if production:
        bot.run(secrets["discord_public_key"])
    else:
        bot.run(secrets["discord_testing_key"])
