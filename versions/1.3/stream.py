import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, guild_only
import praw
import json
from os import path, listdir
from os.path import isfile, join
import time

version = '1.3 Created by bwac#2517'
red = 0xFF0000

secrets = None
with open("/home/bobwithacamera/secrets.json") as json_file:
    secrets = json.load(json_file)

# login to reddit
reddit = praw.Reddit(client_id=secrets["reddit"]["client_id"],
                     client_secret=secrets["reddit"]["client_secret"],
                     user_agent='redditbot created by bwac#2517')


class stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''
        self.index = 0
        self.streamer.start()

    @commands.command(name='startstream')
    @guild_only()
    @has_permissions(manage_channels=True)
    async def startstream(self, ctx, subreddit_name=None):
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Starting...', value='<a:loading:650579775433474088> Starting...')
        loading.set_footer(text="if it never loads, something went wrong, https://rbdis.xyz/bugreport")
        loadingMessage = await ctx.send(embed=loading)
        if subreddit_name:
            exists = True
            if subreddit_name == "all" or subreddit_name == "All":
                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Loading...', value=':no_entry_sign: You cant use r/all')
                loading.set_footer(text=version)
                await loadingMessage.edit(embed=loading)
            else:
                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Adding channel to database...', value='<a:loading:650579775433474088>')
                loading.set_footer(text="if it never loads, something went wrong, https://rbdis.xyz/bugreport")
                await loadingMessage.edit(embed=loading)

                channels = ctx.guild.text_channels
                has_stream = False
                for channel in channels:
                    if str(channel).__contains__('stream'):
                        if ctx.author.id != 408355239108935681:
                            has_stream = True

                if not has_stream:
                    if path.exists('streams/' + subreddit_name + '.json'):
                        with open('streams/' + subreddit_name + '.json') as json_file:
                            stream_dict = json.load(json_file)
                            if str(ctx.guild.id) in stream_dict["channels"]:
                                if len(stream_dict["channels"][str(ctx.guild.id)]) < 1:
                                    channel = await ctx.guild.create_text_channel(subreddit_name + " stream")
                                    stream_dict["channels"][str(ctx.guild.id)].append(channel.id)
                                    with open('streams/' + subreddit_name + '.json', 'w') as json_file:
                                        json.dump(stream_dict, json_file, indent=4)
                                else:
                                    loading = discord.Embed(title='', color=red)
                                    loading.add_field(name='Sorry!', value=":no_entry_sign: you can't have more than 1 "
                                                                           "streams per server (for now)\nIf you have "
                                                                           "a channel with "
                                                                           "'stream' in the name it might break "
                                                                           "things\nA post needs to be made to the "
                                                                           "subreddit for it to update")
                                    loading.set_footer(
                                        text=version)
                                    await loadingMessage.edit(embed=loading)
                            else:
                                channel = await ctx.guild.create_text_channel(subreddit_name + " stream")
                                stream_dict["channels"][str(ctx.guild.id)] = []
                                stream_dict["channels"][str(ctx.guild.id)].append(channel.id)

                                with open('streams/' + subreddit_name + '.json', 'w') as json_file:
                                    json.dump(stream_dict, json_file, indent=4)
                                    loading = discord.Embed(title='', color=red)
                                    loading.add_field(name='Done!',
                                                      value='Your stream will start showing posts in a minute or so\n\n'
                                                            "Please read this info: \n 1. If you added a subreddit "
                                                            "that "
                                                            "doesn't exist it wont work\n2. If you need to make a new "
                                                            "channel for the subreddit, simply delete the channel and "
                                                            "rstartstream (A post needs to be made for it to "
                                                            "update)\n3. Don't change the channel name!")
                                    loading.set_footer(text=version)
                                    await loadingMessage.edit(embed=loading)
                    else:
                        with open('streams/' + subreddit_name + '.json', 'w+') as json_file:
                            channel = await ctx.guild.create_text_channel(subreddit_name + " stream")
                            stream_dict = {
                                "sub name": subreddit_name,
                                "last redeemed": time.time(),
                                "channels": {
                                    ctx.guild.id: [channel.id]
                                }
                            }
                            with open('streams/' + subreddit_name + '.json', 'w') as json_file:
                                json.dump(stream_dict, json_file, indent=4)
                                loading = discord.Embed(title='', color=red)
                                loading.add_field(name='Done!',
                                                  value='Your stream will start showing posts in a minute or so\n\n'
                                                        "Please read this info: \n 1. If you added a subreddit "
                                                        "that "
                                                        "doesn't exist it wont work\n2. If you need to make a new "
                                                        "channel for the subreddit, simply delete the channel and "
                                                        "rstartstream (A post needs to be made for it to "
                                                        "update)\n3. Don't change the channel name!")
                                loading.set_footer(text=version)
                                await loadingMessage.edit(embed=loading)
                else:
                    loading = discord.Embed(title='', color=red)
                    loading.add_field(name='Sorry!', value=":no_entry_sign: you can't have more than 1 "
                                                           "streams per server (for now)\nIf you have a channel with "
                                                           "'stream' in the name it might break things\nA post needs "
                                                           "to be made to the subreddit for it to update")
                    loading.set_footer(
                        text=version)
                    await loadingMessage.edit(embed=loading)

    @tasks.loop(seconds=1.0)
    async def streamer(self):
        print('starting stream_one...')
        self.index += 1
        files_ = [f for f in listdir('streams/') if isfile(join('streams/', f))]
        files = []
        i = 0
        for item in files_:
            item = item[:-5]
            files.append(item)
            i = i + 1
        subs = ''
        i = 0
        for sub in files:
            subs = subs + files[i] + "+"
            i = i + 1
        subs = subs[:-1]
        for sub in files:
            subname = sub
            with open('streams/' + sub + '.json') as json_file:
                dump = json.load(json_file)
                lastredeemed = dump["last redeemed"]
                dump["last redeemed"] = time.time()
                with open('streams/' + sub + '.json', 'w') as json_file:
                    json.dump(dump, json_file, indent=4)

                for submission in reddit.subreddit(sub).new(limit=20):
                    createdon = submission.created_utc
                    if createdon > lastredeemed:
                        await self.post(sub, submission, createdon)

    @streamer.before_loop
    async def before_streamer(self):
        print('stream_one is waiting to start...')
        await self.bot.wait_until_ready()

    async def post(self, sub, submission, createdon):
        url = submission.url
        domain = url.split("://")[1].split("/")[0]
        with open('streams/' + sub + '.json') as json_file:
            subdict = json.load(json_file)
            for server in subdict["channels"]:
                k = 0
                if len(subdict["channels"][server]) > 0 or len(subdict["channels"][server]) == 0:
                    for channelid in subdict["channels"][server]:
                        channel = self.bot.get_channel(channelid)
                        if channel is None:
                            with open('streams/' + sub + '.json', 'w') as json_file:
                                del subdict['channels'][server][k]
                                json.dump(subdict, json_file, indent=4)
                                return
                        else:
                            post = discord.Embed(title='', color=red)
                            post.add_field(name='Loading...',
                                           value='<a:loading:650579775433474088> Loading...')
                            post.set_footer(
                                text="if it never loads, something went wrong, "
                                     "https://rbdis.xyz/bugreport")
                            if channel is not None:
                                postMessage = await channel.send(embed=post)
                        if channel is not None:
                            if str(channel).__contains__('stream'):
                                if domain == 'i.redd.it' or domain == 'i.imgur.com':
                                    post = discord.Embed(title='r/' + sub + ', ' + submission.title,
                                                         color=red)
                                    post.set_image(url=url)
                                    post.add_field(name="Author", value=submission.author)
                                    post.add_field(name="Posted on", value=time.ctime(createdon))
                                    post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                    post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                elif domain.__contains__('reddit.com'):
                                    selftext = submission.selftext
                                    post = discord.Embed(title='r/' + sub + ', ' + submission.title,
                                                         color=red)
                                    post.add_field(name="Author", value=submission.author)
                                    post.add_field(name="Posted on", value=time.ctime(createdon))
                                    if selftext != '':
                                        post.add_field(name='Text:', value=selftext)
                                    post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                    post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                    if len(post) > 2000:
                                        post = discord.Embed(title='r/' + sub + ', ' + submission.title,
                                                             color=red)
                                        post.add_field(name="Author", value=submission.author)
                                        post.add_field(name="Posted on", value=time.ctime(createdon))
                                        post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                        post.add_field(name='error:', value='Text is over 2000')
                                        post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                else:
                                    if domain == 'v.redd.it' or domain.__contains__('youtube'):
                                        post = discord.Embed(title='r/' + sub + ', ' + submission.title,
                                                             color=red)
                                        post.add_field(name="Author", value=submission.author)
                                        post.add_field(name="Posted on", value=time.ctime(createdon))
                                        post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                        post.add_field(name='error', value="RedditBot can't play video (" + domain +
                                                                           ")\nIf you want this in discord upvote this "
                                                                           "https://support.discordapp.com/hc/en-us"
                                                                           "/community/posts/360037387352")
                                        post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                    else:
                                        post = discord.Embed(title='r/' + sub + ', ' + submission.title, color=red)
                                        post.add_field(name="Author", value=submission.author)
                                        post.add_field(name="Posted on", value=time.ctime(createdon))
                                        post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                        post.add_field(name='error', value="RedditBot doesn't support " + domain)
                                        post.add_field(name="request", value="Want this website to be supported? "
                                                                             "https://rbdis.xyz/feedback", inline=False)

                                if channel is not None:
                                    await postMessage.edit(embed=post)
                        k = k + 1

def setup(bot):
    bot.add_cog(stream(bot))
