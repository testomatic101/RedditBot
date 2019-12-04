from discord.ext import commands
import discord
import praw
reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                     client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                     user_agent='redditbot created by bwac#2517')
bot = commands.Bot(command_prefix='!')

version = '1.2.4 (patch 2) Created by bwac#2517'
red = 0xFF0000

bot.remove_command('help')


@commands.command(name='help')
async def help(ctx):
    help = discord.Embed(title="Help:",
                         description="**Welcome to the help page, here you can see all the commands RedditBot has to offer**",
                         color=red)
    help.add_field(name="Help support the bot with a vote", value='http://bit.ly/redditDiscordVote', inline=False)
    help.add_field(name="Help support the bot by donating", value='https://donatebot.io/checkout/611147519317245992', inline=False)
    help.add_field(name="Please give your feedback!", value="with the !feedback [feedback] command!", inline=False)
    help.add_field(name="!help", value="Shows this page", inline=False)

    help.add_field(name="!feedback [feed back here]", value="Give your feed back to the dev", inline=False)
    help.add_field(name="!r/ [sub name here]", value="Gives you some info on a subreddit", inline=False)
    help.add_field(name="!u/ [username here]", value="Gives you some info on a user", inline=False)

    help_user = discord.Embed(title="User commands:",
                              description="**Commands to add accounts and account management**", color=red)
    help_user.add_field(name="!connect [user name here]", value="Connect a reddit connect", inline=False)
    help_user.add_field(name="!unconnect", value="Unconnect the reddit account that you have connected",
                        inline=False)
    help_user.add_field(name="!code", value="Submit the code you got from reddit", inline=False)
    help.add_field(name="!me", value="See your account", inline=False)

    help_user.set_footer(text="RedditBot " + version)
    await ctx.author.send(embed=help)
    await ctx.author.send(embed=help_user)
bot.add_command(help)


@commands.command()
async def feedback(ctx, feedback=None):
    if feedback:
        reddit.redditor('-_-BWAC-_-').message('FeedBack sent by ' + ctx.author.name + '#' + ctx.author.discriminator,
                                              feedback + '\n\nUser Info: \nID: ' + str(ctx.author.id))
        await ctx.author.send('Thanks for the feedback! Hopefully we can get back to you on that. If you want to tell it to the devs face, do that here: discord.gg/62GSYwN.')
    else:
        ctx.send('No feedback given. !feedback [feedback here]')
bot.add_command(feedback)

@commands.command()
async def update(ctx):
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="!help | In " + str(len(bot.guilds)) + " servers"))

extensions = ["user", "subreddit", "connection"]


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

    bot.run("NDM3NDM5NTYyMzg2NTA1NzMw.Xede3A.x8tTiwnZt4VTm_GniqofMe1wGQU")
