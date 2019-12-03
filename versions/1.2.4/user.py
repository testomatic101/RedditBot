import discord
from discord.ext import commands
import praw
import datetime

version = '1.2.4 (patch 1) Created by bwac#2517'
red = 0xFF0000


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='u/')
    async def user(self, ctx, username=None):
        if username:
            loading = discord.Embed(title='', ncolor=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Contacting reddit servers...')
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(client_id='HV16ttsYvjsrRw',
                                 client_secret="StcBK-8Ml-VXM83xFFb0teO5ElM",
                                 password='Redtrucke',
                                 user_agent='reddit',
                                 username='TheRedditBotDiscord')

            loading = discord.Embed(title='', color=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Getting profile info...')
            await loadingMessage.edit(embed=loading)

            user_r = reddit.redditor(username)  # makes user
            user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
            user.add_field(name='Karma:', value=user_r.comment_karma, inline=False)
            user.add_field(name='Link karma:', value=user_r.link_karma, inline=False)
            user.add_field(name='All karma:', value=user_r.link_karma + user_r.comment_karma, inline=False)
            user.add_field(name='Cake Day:', value=datetime.datetime.fromtimestamp(int(user_r.created)).strftime('%m/%d/%Y'), inline=False)
            trophies = []
            for trophy in user_r.trophies():
                trophies.append(trophy.name)
            user.add_field(name='Trophies:', value=trophies, inline=False)

            if user_r.is_employee:
                user.add_field(name='This user is a employee of reddit', inline=False)

            user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
            user.set_thumbnail(url=user_r.icon_img)
            user.set_footer(text="RedditBot " + version)
            await loadingMessage.edit(embed=user)
        else:
            await ctx.send("Sorry, you didn't give a user!")

def setup(bot):
    bot.add_cog(user(bot))
