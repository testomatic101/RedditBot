import discord
from discord.ext import commands
import praw
import random
import datetime
import json
import os

version = '1.2.4 (patch 1) Created by bwac#2517'
red = 0xFF0000


class connection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ''

    @commands.command()
    async def connect(self, ctx, username=None):
        reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                             client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                             user_agent='redditbot')
        
        user_r = reddit.redditor(username)

        code = 0
        code = code + random.randint(1000, 9999)

        data = {
            "registered": str(datetime.datetime.now()),
            "reddit name": username,
            "discord name": ctx.author.name,
            "discord id": ctx.author.id,
            "code": code,
            "connected": False,
            "has +": False
        }

        with open("users/" + str(ctx.author.id) + '.json', 'w+') as outfile:
            json.dump(data, outfile, indent=4)
        reddit.redditor(username).message('Discord user ' + data[
            "discord name"] + ' has tryed to connect to your discord account. Your code for Reddit',
                                           'This is your code: ' + str(
                                               code) + '\n\nIf you are being spammed by codes, dm me here: https://discord.gg/ZmyYxQg')
        await ctx.author.send('You have been sent a code on reddit. Do `!code [code]` to connect your account, if you have already have a connected account, it was removed')

    @commands.command()
    async def unconnect(self, ctx):
        user_id = str(ctx.author.id)
        try:
            os.remove("users/" + user_id + '.json')
            await ctx.channel.send("Done!")
        except FileNotFoundError:
            await ctx.author.send("No pending to be or connected accounts")

    @commands.command()
    async def code(self, ctx, code=None):
        user_id = str(ctx.author.id)
        success = None
        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)
                if user_info["connected"] == True:
                    await ctx.channel.send(ctx.author.mention + " You already have a connected account!")
                    return
                elif str(user_info["code"]) == code:
                    success = True
        except FileNotFoundError:
            await ctx.channel.send(ctx.author.mention + " You haven't requested a code!")
            return
        if success == True:
            filename = "users/" + user_id + '.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                data['connected'] = True  # <--- add `id` value.
            os.remove(filename)
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            await ctx.author.send("Done! Your now connected")
        else:
            await ctx.author.send("Sorry, wrong code")

    @commands.command()
    async def me(self, ctx):
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value='<a:loading:650579775433474088>')
        loadingMessage = await ctx.channel.send(embed=loading)

        user_id = str(ctx.author.id)

        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)

                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Contacting reddit servers...')
                await loadingMessage.edit(embed=loading)

                reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                                     client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                                     user_agent='redditbot')

                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Loading...', value='<a:loading:650579775433474088> Getting your profile info...')
                await loadingMessage.edit(embed=loading)

                user_r = reddit.redditor(user_info['reddit name'])  # makes user
                if user_info["connected"] == False:
                    await ctx.channel.send(ctx.author.mention + ' No connected account')
                    return

                user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
                user.add_field(name='Karma:', value=user_r.comment_karma, inline=False)
                user.add_field(name='Link karma:', value=user_r.link_karma, inline=False)
                user.add_field(name='All karma:', value=user_r.link_karma + user_r.comment_karma, inline=False)
                user.add_field(name='Cake Day:',
                               value=datetime.datetime.fromtimestamp(int(user_r.created)).strftime('%m/%d/%Y'),
                               inline=False)
                trophies = []
                for trophy in user_r.trophies():
                    trophies.append(trophy.name)
                user.add_field(name='Trophies:', value=str(trophies), inline=False)

                if user_r.is_employee:
                    user.add_field(name='You are', value='an employee of reddit!', inline=False)

                user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                user.set_thumbnail(url=user_r.icon_img)
                user.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=user)

                # Update user info if changed
                if user_info["discord name"] != ctx.author.name:
                    user_info["discord name"] = ctx.author.name

                    with open("users/" + str(ctx.author.id) + '.json', 'w+') as outfile:
                        json.dump(user_info, outfile, indent=4)
        except FileNotFoundError:
            await loadingMessage.edit(ctx.author.mention + ' No connected account')

def setup(bot):
    bot.add_cog(connection(bot))
