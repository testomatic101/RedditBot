import discord
from discord.ext import commands
import praw
import datetime
import json

version = '1.2.5 Created by bwac#2517'
red = 0xFF0000

secrets = None
with open('/home/bobwithacamera/secrets.json') as json_file:
    secrets = json.load(json_file)

trophyemojis = None
with open('trophyemoji.json') as json_file:
    trophyemojis = json.load(json_file)


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='u')
    async def user(self, ctx, username=None):
        if username:
            loading = discord.Embed(title='', ncolor=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Contacting reddit servers...')
            loading.set_footer(text="if it never loads, RedditBot can't find the user")
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(client_id=secrets["reddit"]["client_id"],
                                 client_secret=secrets["reddit"]["client_secret"],
                                 user_agent='redditbot created by bwac#2517')

            loading = discord.Embed(title='', color=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Getting profile info...')
            loading.set_footer(text="if it never loads, something went wrong behind the scenes")
            await loadingMessage.edit(embed=loading)

            user_r = reddit.redditor(username)  # makes user
            user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
            user.add_field(name='Karma:', value=user_r.comment_karma)
            user.add_field(name='Link karma:', value=user_r.link_karma)
            user.add_field(name='All karma:', value=user_r.link_karma + user_r.comment_karma)
            user.add_field(name='Cake Day:', value=datetime.datetime.fromtimestamp(int(user_r.created)).strftime('%m'
                                                                                                                 '/%d'
                                                                                                                 '/%Y'))

            trophiestxt = ''
            for trophy in user_r.trophies():
                emoji = ''
                if trophy.name in trophyemojis:
                    emoji = trophyemojis.get(trophy.name)
                if len(trophiestxt) > 900:
                    trophiestxt = trophiestxt + 'All the trophies are too long to send in a discord embed value so I ' \
                                                'shortened them '
                    break
                trophiestxt = trophiestxt + emoji + trophy.name + '\n'
            user.add_field(name='Trophies:', value=trophiestxt)

            if user_r.is_employee:
                user.add_field(name='This user', value='is an employee of reddit', inline=False)

            user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
            user.set_thumbnail(url=user_r.icon_img)
            user.set_footer(text="RedditBot " + version)
            await loadingMessage.edit(embed=user)
        else:
            error = discord.Embed(title="You didn't give a subreddit!\n\nYou should use this command like:\n!r/ ["
                                        "subreddit name]", color=red)
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name='u/')
    async def achivedr(self, ctx):
        await ctx.send('Sorry ru/ has moved to ru')


def setup(bot):
    bot.add_cog(user(bot))
