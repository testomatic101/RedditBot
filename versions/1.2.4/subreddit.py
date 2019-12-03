import discord
from discord.ext import commands
import praw

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
            loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Contacting reddit servers...')
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(client_id='HV16ttsYvjsrRw',
                                 client_secret="StcBK-8Ml-VXM83xFFb0teO5ElM",
                                 password='Redtrucke',
                                 user_agent='reddit',
                                 username='TheRedditBotDiscord')

            subreddit = reddit.subreddit(subreddit_name)  # makes subreddit
            mods = ''
            modAmount = 0
            for moderator in subreddit.moderator():
                modAmount = modAmount + 1
                mods = mods + '\n' + str(moderator)
            if subreddit.over18:
                await ctx.send(
                    ':underage: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:underage:')
                return
            if subreddit_name in ["gory", "watchpeopledie", "gore", "WPDtalk",]:
                await ctx.send(
                    'Sorry ' + ctx.author.mention + 'Due to discords tos (https://discordapp.com/terms) this bot can only show very limited content content')
                sub = discord.Embed(title='**Cant show name due to discord tos** info:', color=red)
                sub.add_field(name='Description snippet:', value='**Cant show description due to discord tos**',
                              inline=False)
                sub.add_field(name='Subscriber Count:', value=subreddit.subscribers, inline=False)
                '''To be worked on: time'''
                # sub.add_field(name='Created on:' , value=created_on_date, inline=False)
                sub.add_field(name='NSFW:', value='No but is on the black list for subs that violate the tos',
                              inline=False)  # add variable here when i add channel nsfw checking
                sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                sub.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=sub)
            else:
                subreddit_description = subreddit.description
                subreddit_description = subreddit_description[:300]
                """To be worked on: time"""
                # created_on = subreddit.created_utc
                # created_on_date = time.strftime("%Y-%m-%d %H:%M:%S", created_on)
                sub = discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
                sub.add_field(name='\nDescription snippet:',
                              value=subreddit_description,
                              inline=False)
                sub.add_field(name='\nSubscriber Count:', value=subreddit.subscribers, inline=False)
                '''To be worked on: time'''
                # sub.add_field(name='Created on:' , value=created_on_date, inline=False)
                sub.add_field(name='NSFW:', value='No',
                              inline=False)  # add variable here when i add channel nsfw checking
                sub.add_field(name='Mods:',
                              value=str(modAmount) + " mods. To see all mods do !mods r/" + subreddit_name,
                              inline=False)
                sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                sub.set_thumbnail(url=subreddit.icon_img)
                sub.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=sub)

def setup(bot):
    bot.add_cog(subreddit(bot))
