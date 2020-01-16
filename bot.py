from discord.ext import commands
import discord
import praw
import dbl
import json
import random

# secrets.json has tokens ect
secrets = None

with open("C:/Users/Noahd/Documents/secrets.json") as json_file:
    secrets = json.load(json_file)

# login to reddit
reddit = praw.Reddit(client_id=secrets["reddit"]["client_id"],
                     client_secret=secrets["reddit"]["client_secret"],
                     user_agent='redditbot created by bwac#2517')
# make the bot client
bot = commands.Bot(command_prefix='r')

# this is used for the footer of embeds
version = '1.3 https://rbdis.xyz redditbot created by bwac#2517'
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
    helpembed = discord.Embed(title="**http://rbdis.xyz**",
                         description="help",
                         color=red)
    botinfo = await topggclient.get_bot_info()
    getto = botinfo.get('monthlyPoints') + 10
    helpembed.add_field(name="\n\nThe bot currently has **" + str(botinfo.get('monthlyPoints')) + "** votes, can we "
                                                                                                  "get it to **" +
                             str(getto) + "**?", value='https://top.gg/bot/437439562386505730/vote', inline=False)
    helpembed.add_field(name="Found a bug?", value="Report it here http://rbdis.xyz/bugreport/", inline=False)
    helpembed.add_field(name="Please give your feedback!", value="http://rbdis.xyz/feedback", inline=False)
    helpembed.add_field(name="rhelp", value="Shows this page", inline=False)

    commandsembed = discord.Embed(title="Help:",
                         description="**Commands for seeing subs and users**",
                         color=red)
    commandsembed.add_field(name="rr [sub name here]", value="Gives you some info on a subreddit", inline=False)
    commandsembed.add_field(name="ru [username here]", value="Gives you some info on a user", inline=False)

    streamembed = discord.Embed(title="",
                         description='NEW **"Stream" commands**',
                         color=red)
    streamembed.add_field(name="rstartstream [sub name here]", value='***BETA*** **STUFF WILL PROBABLY BREAK** '
                                                                     'Streaming '
                                                                     'a subreddit shows all posts made to '
                                                                     'the subreddit automatically to a channel '
                                                                     'created by '
                                                                     'the bot', inline=False)
    await ctx.author.send(embed=helpembed)
    await ctx.author.send(embed=commandsembed)
    await ctx.author.send(embed=streamembed)
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


@bot.event
async def on_ready():
    # make the presence when the bot is ready

    print('ready')
    # print(bot.guilds)
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
    ranint = random.randint(1, 3)
    if ranint == 1:
        votemessage = discord.Embed(title="wanna help out the bot?",
                                  description="if you didnt know, top.gg resets all votes every month. So it would "
                                              "mean even more to me if you voted at "
                                              "https://top.gg/bot/437439562386505730/vote",
                                  color=red)
        await ctx.send(embed=votemessage)
    elif ranint == 2:
        feedbackmessage = discord.Embed(title="Have you found a bug?",
                                    description="report it here http://rbdis.xyz/bugreport",
                                    color=red)
        await ctx.send(embed=feedbackmessage)
    else:
        newmessage = discord.Embed(title="Have you tried the new rstartstream command?",
                                    description="more info on rhelp!",
                                    color=red)
        await ctx.send(embed=newmessage)

# all the cogs
extensions = ["user", "subreddit", "topgg", "stream"]

if __name__ == "__main__":
    # load the cogs
    for extension in extensions:
        bot.load_extension(extension)
    # run the bot
    bot.run(secrets["discord"]["RedditBot"]["testing"])
