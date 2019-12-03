import discord
from discord.ext import commands
import praw

version = '1.2.4'
red = 0xFF0000


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command(name='u/')
    async def user(self, ctx, username=None):
        if username:
            loading = discord.Embed(title='', color=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Contacting reddit servers...')
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                     client_secret="gy6XLBwv_AcRcUZm_fN6Ef-n0Hs",
                     password='Redtrucke2',
                     user_agent='reddit',
                     username='TheRedditBotDiscord')

            loading = discord.Embed(title='', color=red)
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Getting profile info...')
            await loadingMessage.edit(embed=loading)

            user_r = reddit.redditor(username)  # makes user

            user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
            user.add_field(name='Karma:', value=user_r.comment_karma, inline=False)
            user.add_field(name='Link karma:', value=user_r.link_karma, inline=False)

            user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
            user.set_thumbnail(url=user_r.icon_img)
            user.set_footer(text="RedditBot " + version)
            await loadingMessage.edit(embed=user)
        else:
            await ctx.send("Sorry, you didn't give a user!")

def setup(bot):
    bot.add_cog(user(bot))
