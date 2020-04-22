from discord.ext import commands
import discord, random, os, json, dbl


version_number = "1.4.2"
version = version_number + " Created by bwac#2517"
red = 0xFF0000

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True


with open("secrets.json") as json_file:
    secrets = json.load(json_file)

# make the bot client
bot = commands.Bot(command_prefix="r!", help_command=None)

if production:
    # make the top.gg api client
    topggclient = dbl.DBLClient(bot, secrets["topgg_key"])


@commands.command(name="help")
async def newhelp(ctx):
    """Shows all commands"""

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
    commandsembed = discord.Embed(title="Help:", color=red)
    commandsembed.add_field(name="r!help", value="Shows this page", inline=False)
    commandsembed.add_field(
        name="r!about \n*aliases: r!info*",
        value="\nFields: None\nAbout this bot",
        inline=False,
    )
    commandsembed.add_field(
        name="r!subreddit \n*aliases: r!s, r!sub*",
        value="Fields: `sub name`\nGives you some info on a subreddit",
        inline=False,
    )
    commandsembed.add_field(
        name="r!user \n*aliases: r!u*",
        value="Fields: `username`\nGives you some info on a user",
        inline=False,
    )
    commandsembed.add_field(
        name="r!resetsub",
        value="Fields: `subreddit`\nRemoves subreddit cache",
        inline=False,
    )
    commandsembed.add_field(
        name="r!resetuser",
        value="Fields: `username`\nRemoves user cache",
        inline=False,
    )
    commandsembed.add_field(
        name="r!hot \n*aliases: r!h*",
        value="Fields: `subreddit`\nShows the top 10 hot posts",
        inline=False,
    )
    commandsembed.add_field(
        name="r!top \n*aliases: r!t*",
        value="Fields: `subreddit`\nShows the top 10 top posts",
        inline=False,
    )
    commandsembed.add_field(
        name="r!new \n*aliases: r!n*",
        value="Fields: `subreddit`\nShows the top 10 new posts",
        inline=False,
    )
    await ctx.message.add_reaction(emoji="📬")

    await ctx.author.send(embed=helpembed)
    await ctx.author.send(embed=commandsembed)


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
