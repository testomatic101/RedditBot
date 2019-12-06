from discord.ext import commands
import discord
import praw
import dbl
reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                     client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                     user_agent='redditbot created by bwac#2517')
bot = commands.Bot(command_prefix='r')

version = '1.2.4 (patch 5) Created by bwac#2517'
red = 0xFF0000

bot.remove_command('help')

topggclient = dbl.DBLClient(bot, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                                 '.eyJpZCI6IjQzNzQzOTU2MjM4NjUwNTczMCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTc1NTc2MTU1fQ'
                                 '.LbuHaiap7xTKvytdqGnkSpgISUp8cbOzyJ4BETm2eYg')

@commands.command(name='help')
async def help(ctx):
    print(await topggclient.get_bot_info())

    help = discord.Embed(title="Help:",
                         description="**Welcome to the help page, here you can see all the commands RedditBot has to "
                                     "offer**",
                         color=red)
    botinfo = await topggclient.get_bot_info()
    getto = botinfo.get('monthlyPoints') + 10
    help.add_field(name="The bot currently has **" + str(botinfo.get('monthlyPoints')) + "** votes, can we get it to **" + str(getto) + "**?", value='https://top.gg/bot/437439562386505730/vote', inline=False)
    help.add_field(name="Help support the bot by donating", value='https://donatebot.io/checkout/611147519317245992', inline=False)
    help.add_field(name="Please give your feedback!", value="with the rfeedback [feedback] command!", inline=False)
    help.add_field(name="rhelp", value="Shows this page", inline=False)

    help.add_field(name="rfeedback [feed back here]", value="Give your feed back to the dev", inline=False)
    help.add_field(name="rr [sub name here]", value="Gives you some info on a subreddit", inline=False)
    help.add_field(name="ru [username here]", value="Gives you some info on a user", inline=False)

    help_user = discord.Embed(title="User commands:",
                              description="**Commands to add accounts and account management**", color=red)
    help_user.add_field(name="rconnect [user name here]", value="Connect a reddit connect", inline=False)
    help_user.add_field(name="runconnect", value="Unconnect the reddit account that you have connected",
                        inline=False)
    help_user.add_field(name="rcode", value="Submit the code you got from reddit", inline=False)
    help.add_field(name="rme", value="See your account", inline=False)

    help_user.set_footer(text="RedditBot " + version)
    await ctx.author.send(embed=help)
    await ctx.author.send(embed=help_user)
bot.add_command(help)


@commands.command()
async def feedback(ctx, feedback=None):
    if feedback:
        reddit.redditor('-_-BWAC-_-').message('FeedBack sent by ' + ctx.author.name + '#' + ctx.author.discriminator,
                                              feedback + '\n\nUser Info: \nID: ' + str(ctx.author.id))
        await ctx.author.send('Thanks for the feedback! Hopefully we can get back to you on that. If you want to tell '
                              'it to the devs face, do that here: discord.gg/62GSYwN.')
    else:
        ctx.send('No feedback given. rfeedback [feedback here]')
bot.add_command(feedback)

@commands.command()
async def update(ctx):
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="rhelp | In " + str(len(bot.guilds)) + " servers"))
bot.add_command(update)

extensions = ["user", "subreddit", "connection", "topgg"]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    print('Servers connected to:')
    print(len(bot.guilds))

    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="!help | In " + str(len(bot.guilds)) + " servers"))
if __name__ == "__main__":
    if __name__ == '__main__':
        for extension in extensions:
            bot.load_extension(extension)
    #NjUwNTgzNzk5MDQxNjIyMDQ2.XegePg.9AsWwPevhV6QrSG-Dk0SecyrqLw
    #NDM3NDM5NTYyMzg2NTA1NzMw.XemCLQ.xeC39YxL2O1gLfAH1bgnDa5JQsg
    bot.run("NDM3NDM5NTYyMzg2NTA1NzMw.XemCLQ.xeC39YxL2O1gLfAH1bgnDa5JQsg")
