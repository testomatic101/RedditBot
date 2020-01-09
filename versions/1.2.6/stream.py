import discord
from discord import ChannelType
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions, guild_only
import praw
import json
from os import path, remove, listdir
from os.path import isfile, join
import asyncio

version = '1.2.6 Created by bwac#2517'
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
                                                                           "streams per server (for now)")
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
                                                            "**Please read this info: \n 1. If you added a subreddit "
                                                            "that "
                                                            "doesn't exist it wont work\n2. If you need to make a new "
                                                            "channel for the subreddit, simply delete the channel and "
                                                            "rstartstream** *(A post needs to be made for it to "
                                                            "update)*\n**3. Don't change the channel name!**")
                                    loading.set_footer(text=version)
                                    await loadingMessage.edit(embed=loading)
                    else:
                        with open('streams/' + subreddit_name + '.json', 'w+') as json_file:
                            channel = await ctx.guild.create_text_channel(subreddit_name + " stream")
                            stream_dict = {
                                "sub name": subreddit_name,
                                "channels": {
                                    ctx.guild.id: [channel.id]
                                }
                            }
                            with open('streams/' + subreddit_name + '.json', 'w') as json_file:
                                json.dump(stream_dict, json_file, indent=4)
                                loading = discord.Embed(title='', color=red)
                                loading.add_field(name='Done!',
                                                  value='Your stream will start showing posts in a minute or so\n\n'
                                                        "**Please read this info: \n 1. If you added a subreddit that "
                                                        "doesn't exist it 'wont work\n2. If you need to make a new "
                                                        "channel for the subreddit, simply delete the channel and "
                                                        "rstartstream **(A post needs to be made for it to "
                                                        "update)**\n3. Don't change the channel name!")
                                loading.set_footer(text=version)
                                await loadingMessage.edit(embed=loading)
                else:
                    loading = discord.Embed(title='', color=red)
                    loading.add_field(name='Sorry!', value=":no_entry_sign: you can't have more than 1 "
                                                           "streams per server (for now)\nIf you have a channel with "
                                                           "'stream' in the name it might break things")
                    loading.set_footer(
                        text=version)
                    await loadingMessage.edit(embed=loading)

    @tasks.loop(seconds=5.0)
    async def streamer(self):
        self.index += 1
        files_ = [f for f in listdir('streams/') if isfile(join('streams/', f))]
        files = []
        for item in files_:
            item = item[:-5]
            files.append(item)
        subs = ''
        i = 0
        for sub in files:
            subs = subs + files[i] + "+"
            i = i + 1
        subs = subs[:-1]
        j = 0
        for submission in reddit.subreddit(subs).stream.submissions():
            if j > 50:
                break
            print(j)
            j = j + 1
            subname = submission.subreddit.display_name
            with open('streams/' + subname + '.json') as json_file:
                subdict = json.load(json_file)
                for server in subdict["channels"]:
                    k = 0
                    for channelid in subdict["channels"][server]:
                        channel = self.bot.get_channel(channelid)
                        if channel is None:
                            # Only works if limit is one
                            del subdict['channels'][server]
                            with open('streams/' + subname + '.json', 'w') as json_file:
                                json.dump(subdict, json_file, indent=4)
                            break
                        if str(channel).__contains__('stream'):
                            url = str(submission.url)
                            post = discord.Embed(title='', color=red)
                            post.add_field(name='Loading...', value='<a:loading:650579775433474088> Loading...')
                            post.set_footer(
                                text="if it never loads, something went wrong, https://rbdis.xyz/bugreport")
                            postMessage = await channel.send(embed=post)
                            if submission.is_self:
                                selftext = submission.selftext
                                post = discord.Embed(title='r/' + subname + ', ' + submission.title, color=red)
                                if selftext != '':
                                    post.add_field(name='Text:', value=selftext)
                                post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                await postMessage.edit(embed=post)
                            elif url.__contains__('.jpg') or url.__contains__('.png') or url.__contains__('.jpeg') or url.__contains__('.tiff'):
                                post = discord.Embed(title='r/' + subname + ', ' + submission.title, color=red)
                                post.set_image(url=url)
                                post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                await postMessage.edit(embed=post)
                            elif selftext:
                                post = discord.Embed(title='r/' + subname + ', ' + submission.title, color=red)
                                post.add_field(name='Text', value=selftext)
                                post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                await postMessage.edit(embed=post)
                            else:
                                post = discord.Embed(title='r/' + subname + ', ' + submission.title, color=red)
                                post.add_field(name='Link:', value=submission.shortlink, inline=False)
                                post.set_footer(text="something wrong? https://rbdis.xyz/bugreport")
                                await postMessage.edit(embed=post)
                        else:
                            with open('streams/' + subname + '.json', 'w') as json_file:
                                del subdict['channels'][server][k]
                                json.dump(subdict, json_file, indent=4)
                        k = k + 1

    @streamer.before_loop
    async def before_streamer(self):
        print('waiting...')
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(stream(bot))
