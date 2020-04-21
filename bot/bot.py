from discord.ext import commands
import discord, praw, json, random, dbl, os, uuid

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True


with open("secrets.json") as json_file:
    secrets = json.load(json_file)

# this is used for the footer of embeds
version_number = "1.4.2"
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
    helpembed = discord.Embed(title="**http://rbdis.xyz**", description="", color=red)
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
        name="Want to give your feedback? Or have you found a bug that needs fixing?",
        value="http://rbdis.xyz/feedback",
        inline=False,
    )

    commandsembed = discord.Embed(title="Help:", description="**Commands**", color=red)
    commandsembed.add_field(name="r!help", value="Shows this page", inline=False)
    commandsembed.add_field(
        name="r!about", value="About this bot\n*aliases: about, info*", inline=False
    )
    commandsembed.add_field(
        name="r!subreddit `sub name here (no spaces)`\n*aliases: s, sub*",
        value="Gives you some info on a subreddit",
        inline=False,
    )
    commandsembed.add_field(
        name="r!user `username here (no spaces)`\n*aliases: u*",
        value="Gives you some info on a user",
        inline=False,
    )
    commandsembed.add_field(
        name="r!resetsub `sub name here (no spaces)`",
        value="Removes subreddit cache",
        inline=False,
    )
    commandsembed.add_field(
        name="r!resetuser `user name here (no spaces)`",
        value="Removes user cache",
        inline=False,
    )
    commandsembed.add_field(
        name="r!hot `**subreddit** name here (no spaces)`\n*aliases: h*",
        value="Shows the top 10 hot posts",
        inline=False,
    )
    commandsembed.add_field(
        name="r!top `**subreddit** name here (no spaces)`\n*aliases: t*",
        value="Shows the top 10 top posts",
        inline=False,
    )
    commandsembed.add_field(
        name="r!new `**subreddit** name here (no spaces)`\n*aliases: n*",
        value="Shows the top 10 new posts",
        inline=False,
    )

    await ctx.send(embed=helpembed)
    await ctx.send(embed=commandsembed)


# add the about command
bot.add_command(newhelp)


@commands.command(aliases=["info"])
async def about(ctx):
    about = discord.Embed(
        title="About",
        description="Hey, im RedditBot!\nIm made by bwac#2517\nIm currently running version "
        + version_number
        + "\nIm in "
        + str(len(bot.guilds))
        + " servers"
        + "\nMy site is https://rbdis.xyz\nIm made using discord.py\nMy github is https://github.com/BWACpro/RedditBot",
        color=red,
    )
    await ctx.send(embed=about)


# add the new help command
bot.add_command(about)

# clear cache/temp files (only for bwac)
@commands.command()
async def clear(ctx, what_to_clear=None):
    if ctx.author.id == 408355239108935681:
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


# add the clear command
bot.add_command(clear)


@bot.event
async def on_command_error(ctx, error):
    """Sends error to user and channel"""

    id = ""
    if production:
        id = "P"
    else:
        id = "B"
    id = id + str(uuid.uuid4().hex)

    if str(error).__contains__("Command ") and str(error).__contains__("is not found"):
        await ctx.send(
            str(ctx.author)
            + " I can't find that command..\nIf you think it should exist https://rbdis.xyz/bugreport\nID: "
            + id
        )
        await bot.get_channel(700277796148215838).send(
            "Author: "
            + str(ctx.author)
            + "\nText: "
            + ctx.message.content
            + "\nCommand doesnt exist\nID: "
            + id
        )
    elif (
        str(error)
        == "Command raised an exception: Redirect: Redirect to /subreddits/search"
    ):
        await ctx.send(
            str(ctx.author)
            + " Something went wrong, its probably because of a nonexistent or unreachable subreddit..\nIf you think something is broken https://rbdis.xyz/bugreport\nID: "
            + id
        )
        await bot.get_channel(700277796148215838).send(
            "Author: "
            + str(ctx.author)
            + "\nText: "
            + ctx.message.content
            + "\nCommand doesnt exist\nID: "
            + id
        )
    else:
        await ctx.send(
            str(ctx.author)
            + ", something went wrong. \n`"
            + str(error)
            + "`\nIf it keeps happening report it here https://rbdis.xyz/bugreport or https://rbdis.xyz/server\nID: "
            + id
        )
        await bot.get_channel(700277796148215838).send(
            "Author: "
            + str(ctx.author)
            + "\nText: "
            + ctx.message.content
            + "\nError:\n```"
            + str(error)
            + "```\bID: "
            + id
        )


@bot.event
async def on_guild_join(guild):
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

    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=discord.Game(name="r!help | In " + str(len(bot.guilds)) + " servers"),
    )


if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    if production:
        bot.run(secrets["discord_public_key"])
    else:
        bot.run(secrets["discord_testing_key"])
