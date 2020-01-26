import discord
from discord.ext import commands
import praw
import datetime
import json
from sys import platform

version = '1.3 Created by bwac#2517'
red = 0xFF0000

from pathlib import Path
# secrets.json has tokens ect
secrets = None
with open("/home/ubuntu/secrets.json") as json_file:
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

                reddit = praw.Reddit(client_id=secrets["reddit"]["client_id"],
                                     client_secret=secrets["reddit"]["client_secret"],
                                     user_agent='redditbot created by bwac#2517')

                subreddit = reddit.subreddit(subreddit_name)
                if ctx.channel.is_nsfw():
                    datetime.datetime.fromtimestamp(int(subreddit.created_utc)).strftime('%m/%d/%Y')
                    sub = discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
                    sub.add_field(name='\nSmall Description:', value=subreddit.public_description, inline=False)
                    sub.add_field(name='\nSubscriber Count:', value=subreddit.subscribers)
                    sub.add_field(name='NSFW:', value=subreddit.over18)
                    sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                    sub.set_thumbnail(url=subreddit.icon_img)
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
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\n!r/ ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)

def setup(bot):
    bot.add_cog(subreddit(bot))
