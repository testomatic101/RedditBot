from discord.ext import commands
import discord
import praw
import dbl
import json
import random
from sys import platform

# secrets.json has tokens ect
secrets = None
if platform == "win32" or "win32":
    with open('C:/Users/Noahd/Documents/secrets.json') as json_file:
        secrets = json.load(json_file)
else:
    with open('/home/bobwithacamera/secrets.json') as json_file:
        secrets = json.load(json_file)

# login to reddit
reddit = praw.Reddit(client_id=secrets["reddit"]["client_id"],
                     client_secret=secrets["reddit"]["client_secret"],
                     user_agent='redditbot created by bwac#2517')
# make the bot client
bot = commands.Bot(command_prefix='r')

# this is used for the footer of embeds
version = '1.2.5 Created by bwac#2517'
# red for embeds
red = 0xFF0000

# make the top.gg api client
topggclient = dbl.DBLClient(bot, secrets["top.gg"]["token"])

# remove the help so we can have a custom one
bot.remove_command('help')


@commands.command(name='help')
async def newhelp(ctx):
    # custom help command

    # make the embeds
    helpembed = discord.Embed(title="Help:",
                         description="**Welcome to the help page, here you can see all the commands RedditBot has to "
                                     "offer**",
                         color=red)
    botinfo = await topggclient.get_bot_info()
    getto = botinfo.get('monthlyPoints') + 10
    helpembed.add_field(name="\n\nThe bot currently has **" + str(botinfo.get('monthlyPoints')) + "** votes, can we get it to **" + str(getto) + "**?", value='https://top.gg/bot/437439562386505730/vote', inline=False)
    helpembed.add_field(name="Help support the bot by donating", value='https://donatebot.io/checkout/611147519317245992', inline=False)
    helpembed.add_field(name="Please give your feedback!", value="with the rfeedback [feedback] command!", inline=False)
    helpembed.add_field(name="rhelp", value="Shows this page", inline=False)

    helpembed.add_field(name="rfeedback [feed back here]", value="Give your feed back to the dev", inline=False)
    helpembed.add_field(name="rr [sub name here]", value="Gives you some info on a subreddit", inline=False)
    helpembed.add_field(name="ru [username here]", value="Gives you some info on a user", inline=False)

    help_user = discord.Embed(title="User commands:",
                              description="**Commands to add accounts and account management**", color=red)
    help_user.add_field(name="rconnect [user name here]", value="Connect a reddit connect", inline=False)
    help_user.add_field(name="runconnect", value="Unconnect the reddit account that you have connected",
                        inline=False)
    help_user.add_field(name="rcode", value="Submit the code you got from reddit", inline=False)
    help_user.add_field(name="rme", value="See your account", inline=False)

    help_user.set_footer(text="RedditBot " + version)
    await ctx.author.send(embed=helpembed)
# add the new help command
bot.add_command(newhelp)


# the feedback command is for users to send feedback
@commands.command()
async def feedback(ctx, text=None):
    if text:
        reddit.redditor('-_-BWAC-_-').message('FeedBack sent by ' + ctx.author.name + '#' + ctx.author.discriminator,
                                              text + '\n\nUser Info: \nID: ' + str(ctx.author.id))
        await ctx.author.send('Thanks for the feedback! Hopefully we can get back to you on that. If you want to tell '
                              'it to the devs face, do that here: discord.gg/62GSYwN.')
    else:
        ctx.send('No feedback given. rfeedback [feedback here]')
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
    for guild in bot.guilds:
        for invite in await guild.invites():
            print(invite)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="rhelp | In " + str(len(bot.guilds)) + " servers"))


@bot.event
async def on_command_completion(ctx):
    votemessage = discord.Embed(title="wanna help out the bot?",
                              description="if you like the bot, it would mean a lot to the dev if you voted at https://top.gg/bot/437439562386505730/vote",
                              color=red)
    await ctx.send(embed=votemessage)

if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    bot.run(secrets["discord"]["RedditBot"]["production"])
