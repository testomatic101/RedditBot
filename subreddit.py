import discord
from discord.ext import commands
import praw
import datetime
import json
import os

version_number = '1.3.2'
version = version_number + ' Created by bwac#2517'
red = 0xFF0000

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True

with open("secrets.json") as json_file:
    secrets = json.load(json_file)


class subreddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='r')
    async def subreddit(self, ctx, subreddit_name=None):

        if subreddit_name:
            if ctx.guild:
                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Loading...', value="<a:loading:650579775433474088> Contacting reddit "
                                                           "servers...")
                loading.set_footer(text="if it never loads, RedditBot can't find the subreddit")
                loadingMessage = await ctx.send(embed=loading)

                reddit = praw.Reddit(client_id=secrets["reddit_id"],
                                     client_secret=secrets["reddit_secret"],
                                     user_agent='discord:n/a:' + version_number + ' (by /u/-_-BWAC-_-)')

                subreddit = reddit.subreddit(subreddit_name)
                if ctx.channel.is_nsfw():
                    loading = discord.Embed(title='', color=red)
                    loading.add_field(name='Cache...', value="<a:loading:650579775433474088> checking if this has been cached")
                    loading.set_footer(text="if it never loads, something went wrong in the backround, or the subreddit cant be found")
                    await loadingMessage.edit(embed=loading)

                    time_cached = None
                    smalldes = None
                    subcount = None
                    nsfw = None
                    thumbnail = None

                    if os.path.isfile("cache/subreddits/" + subreddit_name + ".json"):
                        # If cache exists, read from it
                        loading = discord.Embed(title='', color=red)
                        loading.add_field(name='Cache...', value="<a:loading:650579775433474088> cache found! now loading from")
                        loading.set_footer(text="if it never loads, something went wrong in the backround, or the subreddit cant be found")
                        await loadingMessage.edit(embed=loading)

                        with open("cache/subreddits/" + subreddit_name + ".json") as json_file:
                            cache = json.load(json_file)

                            time_cached = cache["time_cached"]
                            smalldes = cache["smalldes"]
                            subcount = cache["subcount"]
                            nsfw = cache["nsfw"]
                            thumbnail = cache["thumbnail"]
                    else:
                        # If cache doesnt exit, make it
                        loading = discord.Embed(title='', color=red)
                        loading.add_field(name='Cache...', value="<a:loading:650579775433474088> cache not found.. creating")
                        loading.set_footer(text="if it never loads, something went wrong in the backround, or the subreddit cant be found")
                        await loadingMessage.edit(embed=loading)

                        try:
                            smalldes = subreddit.public_description
                        except:
                            smalldes = None
                        subcount = subreddit.subscribers
                        nsfw = subreddit.over18
                        thumbnail = subreddit.icon_img

                        cache = {
                            'time_cached': str(datetime.datetime.now()),
                            'smalldes': smalldes,
                            'subcount': subcount,
                            'nsfw': nsfw,
                            'thumbnail': thumbnail
                        }
                        print(cache)
                        with open("cache/subreddits/" + subreddit_name + ".json", 'w') as outfile:
                            json.dump(cache, outfile)

                    datetime.datetime.fromtimestamp(int(subreddit.created_utc)).strftime('%m/%d/%Y')
                    sub = discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
                    if smalldes:
                        sub.add_field(name='\nSmall Description:', value=smalldes, inline=False)
                    else:
                        sub.add_field(name='\There is no small description for this subreddit', value="*nothing*", inline=False)
                    sub.add_field(name='\nSubscriber Count:', value=subcount)
                    sub.add_field(name='NSFW:', value=nsfw)
                    if time_cached:
                        sub.add_field(name='*these results are from a cache made at*:', value=time_cached, inline=False)
                        sub.add_field(name='*if you want the latest stats, use rresetsub ' + subreddit_name + '*', value="keep in mind that you should only reset a subreddit cache every so often", inline=False)

                    sub.add_field(name="maybe try:", value="try rhot "+subreddit_name+" and rtop "+subreddit_name+" to show the top 10 top and hot posts", inline=False)

                    sub.set_author(name="RedditBot", icon_url="https://images.discordapp.net/avatars/437439562386505730/2874f76dd780cb0af624e3049a6bfad0.png")
                    sub.set_thumbnail(url=thumbnail)
                    sub.set_footer(text="RedditBot " + version)
                    await loadingMessage.edit(embed=sub)
                else:
                    error = discord.Embed(title='Error', color=red)
                    error.add_field(name='Sorry',
                                    value="The channel **" + ctx.channel.name + "** is not nsfw, to be safe "
                                                                                "with the discord tos and "
                                                                                "such, you will have to "
                                                                                "change the channel to nsfw.")
                    await loadingMessage.edit(embed=error)
            else:
                await ctx.send('Please do this in a server')
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\nrr ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)


    @commands.command(name='top')
    async def top(self, ctx, subreddit_name=None):
        """get the top posts of a subreddit, rtop"""

        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value="<a:loading:650579775433474088> Contacting reddit "
                                                   "servers...")
        loading.set_footer(text="if it never loads, RedditBot can't find the subreddit, or something broke")
        loadingMessage = await ctx.send(embed=loading)

        if subreddit_name:
            reddit = praw.Reddit(client_id=secrets["reddit_id"],
                                 client_secret=secrets["reddit_secret"],
                                 user_agent='discord:n/a:' + version_number + ' (by /u/-_-BWAC-_-)')

            embed = discord.Embed(title="r/"+subreddit_name+"'s top 10 top posts as of right now",
                                description="", color=red)

            for submission in reddit.subreddit(subreddit_name).top(limit=10):
                if len(embed) < 6000:
                    embed.description = embed.description + "\n\n["+submission.title+"](https://reddit.com"+submission.permalink+")\n:thumbsup:"+str(submission.score)+", u/"+str(submission.author)+", "+str(datetime.datetime.fromtimestamp(submission.created_utc).strftime('%m/%d/%Y'))
                await loadingMessage.edit(embed=embed)
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\nrtop ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name='hot')
    async def hot(self, ctx, subreddit_name=None):
        """get the current hot posts of a subreddit, rhot"""

        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value="<a:loading:650579775433474088> Contacting reddit "
                                                   "servers...")
        loading.set_footer(text="if it never loads, RedditBot can't find the subreddit, or something broke")
        loadingMessage = await ctx.send(embed=loading)


        if subreddit_name:
            if ctx.channel.is_nsfw():
                reddit = praw.Reddit(client_id=secrets["reddit_id"],
                                    client_secret=secrets["reddit_secret"],
                                    user_agent='discord:n/a:' + version_number + ' (by /u/-_-BWAC-_-)')

                embed = discord.Embed(title="r/"+subreddit_name+"'s top 10 hot posts as of right now",
                                    description="", color=red)
                for submission in reddit.subreddit(subreddit_name).hot(limit=10):
                    if len(embed) < 6000:
                        embed.description = embed.description + "\n\n["+submission.title+"](https://reddit.com"+submission.permalink+")\n:thumbsup:"+str(submission.score)+", u/"+str(submission.author)+", "+str(datetime.datetime.fromtimestamp(submission.created_utc).strftime('%m/%d/%Y'))
                    await loadingMessage.edit(embed=embed)
            else:
                error = discord.Embed(title='Error', color=red)
                error.add_field(name='Sorry',
                                value="The channel **" + ctx.channel.name + "** is not nsfw, to be safe "
                                                                            "with the discord tos and "
                                                                            "such, you will have to "
                                                                            "change the channel to nsfw.")
                await loadingMessage.edit(embed=error)
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\nrhot ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)


    @commands.command(name='resetsub')
    async def resetsub(self, ctx, subreddit_name=None):
        """resets a subreddit cache"""

        if subreddit_name:
                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Deleting cache...', value="<a:loading:650579775433474088>")
                loading.set_footer(text="if it never loads, RedditBot can't find the subreddit")
                loadingMessage = await ctx.send(embed=loading)

                if os.path.isfile("cache/subreddits/" + subreddit_name + ".json"):
                    os.remove("cache/subreddits/" + subreddit_name + ".json")

                    loading = discord.Embed(title='', color=red)
                    loading.add_field(name='Deleted!...', value="now say rr " + subreddit_name)
                    await loadingMessage.edit(embed=loading)
                else:
                    loading = discord.Embed(title='', color=red)
                    loading.add_field(name='No cache!...', value="try saying rr " + subreddit_name)
                    await loadingMessage.edit(embed=loading)
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\nresetsub ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(subreddit(bot))
