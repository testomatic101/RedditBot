import discord
from discord.ext import commands
import praw
import datetime
from prawcore import NotFound

version = '1.2.4 (patch 1) Created by bwac#2517'
red = 0xFF0000


class subreddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='r/')
    async def subreddit(self, ctx, subreddit_name=None):
        if subreddit_name:
            loading = discord.Embed(title='', color=red)
            loading.add_field(name='Loading...', value="<a:loading:650579775433474088> Contacting reddit "
                                                       "servers...")
            loading.set_footer(text="if it never loads, RedditBot can't find the subreddit")
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                                 client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                                 user_agent='redditbot')

            subreddit = reddit.subreddit(subreddit_name)  # makes subreddit

            if subreddit.over18:
                await ctx.send(
                    ':underage: this is subreddit has been marked as nsfw! If you really what to see that, '
                    'go to reddit your self!:underage:')
                return
            if subreddit_name in ["gory", "watchpeopledie", "gore", "WPDtalk"]:
                await ctx.send(
                    'Sorry ' + ctx.author.mention + 'Due to discords tos (https://discordapp.com/terms) this bot can '
                                                    'only show very limited content content')
                sub = discord.Embed(title='**Cant show name due to discord tos** info:', color=red)
                sub.add_field(name='Short Description:', value='**Cant show description due to discord tos**',
                              inline=False)
                sub.add_field(name='Subscriber Count:', value=subreddit.subscribers, inline=False)

                datetime.datetime.fromtimestamp(int(subreddit.created_utc)).strftime('%m/%d/%Y')

                sub.add_field(name='NSFW:', value='No, but is on the black list for subs that violate the discord tos',
                              inline=False)  # add variable here when i add channel nsfw checking
                sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                sub.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=sub)
            else:
                datetime.datetime.fromtimestamp(int(subreddit.created_utc)).strftime('%m/%d/%Y')

                sub = discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
                sub.add_field(name='\nSmall Description:', value=subreddit.public_description, inline=False)

                sub.add_field(name='\nSubscriber Count:', value=subreddit.subscribers, inline=False)
                '''To be worked on: time'''
                sub.add_field(name='NSFW:', value='No',
                              inline=False)
                sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                sub.set_thumbnail(url=subreddit.icon_img)
                sub.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=sub)
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\n!r/ ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(subreddit(bot))
