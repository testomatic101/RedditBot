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

# all the cogs
extensions = ["cogs.user", "cogs.subreddit", "cogs.utils", "cogs.events"]
if production:
    extensions.append("cogs.topgg")


if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    if production:
        bot.run(secrets["discord_public_key"])
    else:
        bot.run(secrets["discord_testing_key"])
