# https://discordapp.com/api/oauth2/authorize?client_id=437439562386505730&permissions=8&scope=bot
import datetime
import json
import os
import random

import discord
import praw

client = discord.Client()

reddit = praw.Reddit(client_id='HV16ttsYvjsrRw',
                     client_secret="StcBK-8Ml-VXM83xFFb0teO5ElM",
                     password='Redtrucke',
                     user_agent='reddit',
                     username='TheRedditBotDiscord')

version = '1.2.3'

red = 0xFF0000

# black list
black_list = ["gory", "watchpeopledie", "gore", "WPDtalk"]


@client.event
async def on_message(message):
    # admin commands:
    if message.content.startswith('!setstatus') and message.author.id == 408355239108935681:
        status = message.content.replace('!setstatus ', '')
        activity = discord.Game(name=status)
        print("Setting status to '" + str(activity) + "'")
        await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    if message.content.startswith('!refreshstatus') and message.author.id == 408355239108935681:
        activity = discord.Game(name="!help | In " + str(len(client.guilds)) + " servers")
        print("Setting status to '" + str(activity) + "'")
        await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)

    if message.content.startswith('!feedback'):
        feedback = message.content.replace('!feedback ', '')

        reddit.redditor('-_-BWAC-_-').message('FeedBack sent by ' + message.author.name, feedback + '\n\nUser Info: \nID: ' + str(message.author.id))
        await message.channel.send(message.author.mention + ' thanks for the feedback! If you want to tell it to the devs face, do that here: discord.gg/ZmyYxQg.')



    # user commands:
    if message.content.startswith('!help'):
        help = discord.Embed(title="Help:",
                             description="**Welcome to the help page, here you can see all the commands Reddit has to offer**",
                             color=red)
        help.add_field(name="!help", value="Shows this page", inline=False)
        help.add_field(name="!feedback [feed back here]", value="Give your feed back to the dev", inline=False)
        help.add_field(name="!r/[sub name here]", value="Gives you some info on a subreddit", inline=False)
        help.add_field(name="!u/[username here]", value="Gives you some info on a user", inline=False)
        help.add_field(name="!meme", value="Gives a random meme from /r/dankmemes on reddit!", inline=False)
        help.add_field(name="!me", value="See your account", inline=False)

        help_user = discord.Embed(title="User commands:",
                                  description="**Commands to add accounts and account management**", color=red)
        help_user.add_field(name="!connect u/[user name here]", value="Connect a reddit connect", inline=False)
        help_user.add_field(name="!unconnect", value="Unconnect the reddit account that you have connected",
                            inline=False)
        help_user.add_field(name="!code", value="Submit the code you got from reddit", inline=False)

        help_user.set_footer(text="RedditBot " + version)
        await message.author.send(embed=help)
        await message.author.send(embed=help_user)
        await message.author.send(
            "Give your feed back with the !feedback command! \n\nLike the bot? Support it with a vote! http://bit.ly/redditDiscordVote")

    if message.content == '!meme':
        random_post = reddit.subreddit('dankmemes').random()
        random_post_url = random_post.url
        await message.channel.send(random_post_url)

    # Subreddit Commands
    if message.content.startswith('!r/'):
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value='<a:loading:596157264788979750>')
        loadingMessage = await message.channel.send(embed=loading)

        subreddit_name = message.content.replace("!r/", "")  # removes r/
        subreddit = reddit.subreddit(subreddit_name)  # makes subreddit
        mods = ''
        modAmount = 0
        for moderator in subreddit.moderator():
            modAmount = modAmount + 1
            mods = mods + '\n' + str(moderator)
        if subreddit.over18:
            await message.channel.send(
                ':underage: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:underage:')
            return
        if subreddit_name in black_list:
            await message.channel.send(
                'Sorry ' + message.author.mention + 'Due to discords tos (https://discordapp.com/terms) this bot can only show very limited content content')
            """To be worked on: time"""
            # created_on = subreddit.created_utc
            # created_on_date = time.strftime("%Y-%m-%d %H:%M:%S", created_on)

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

            sub.add_field(name='NSFW:', value='No', inline=False)  # add variable here when i add channel nsfw checking

            sub.add_field(name='Mods:', value=str(modAmount) + " mods. To see all mods do !mods r/" + subreddit_name,
                          inline=False)

            sub.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")

            sub.set_thumbnail(url=subreddit.icon_img)
            sub.set_footer(text="RedditBot " + version)
            await loadingMessage.edit(embed=sub)

    if message.content.startswith('!mods'):
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value='<a:loading:596157264788979750>')
        loadingMessage = await message.channel.send(embed=loading)

        if message.content == "!mods":
            await message.channel.send("No subreddit given")
        else:
            subreddit_name = message.content.replace("!mods r/", "")  # removes r/
            subreddit = reddit.subreddit(subreddit_name)  # makes subreddit
            if subreddit.over18:
                await message.channel.send(
                    ':underage: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:underage:')
            else:
                mods = ''
                modAmount = 0
                for moderator in subreddit.moderator():
                    modAmount = modAmount + 1
                    mods = mods + '\n' + str(moderator)

                modMessage = discord.Embed(title=subreddit_name + "'s mods:", color=red)
                modMessage.add_field(name='Mods:', value=modAmount,
                                     inline=False)

                modMessage.add_field(name='Mod Names:', value=mods, inline=False)

                modMessage.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                modMessage.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=modMessage)

    if message.content.startswith('!u/'):
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value='<a:loading:596157264788979750>')
        loadingMessage = await message.channel.send(embed=loading)

        user_name = message.content.replace("!u/", "")  # removes u/
        user_r = reddit.redditor(user_name)  # makes user

        '''to be worked on, is gold?'''
        # user_gold = ''
        # if user_r.is_gold == False:
        # user_gold == 'No'
        # else:
        # user_gold == 'yes'
        user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
        user.add_field(name='Karma:', value=user_r.comment_karma, inline=False)
        user.add_field(name='Link karma:', value=user_r.link_karma, inline=False)
        # user.add_field(name='<:gold:5367939581571542016>\nHas gold?:', value=user_gold, inline=False)

        user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
        user.set_thumbnail(url=user_r.icon_img)
        user.set_footer(text="RedditBot " + version)
        await loadingMessage.edit(embed=user)

    if message.content.startswith('!me') and message.content == "!me":
        loading = discord.Embed(title='', color=red)
        loading.add_field(name='Loading...', value='<a:loading:596157264788979750>')
        loadingMessage = await message.channel.send(embed=loading)

        user_id = str(message.author.id)

        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)
                user_r = reddit.redditor(user_info['reddit name'])  # makes user
                if user_info["connected"] == False:
                    await message.channel.send(message.author.mention + ' No connected account')
                    return

                # to be worked on, is gold?
                # user_gold = ''
                # if user_r.is_gold == False:
                # user_gold == 'No'
                # else:
                # user_gold == 'yes'

                user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
                user.add_field(name='Karma:', value=user_r.comment_karma, inline=False)
                user.add_field(name='Link karma:', value=user_r.link_karma, inline=False)
                # user.add_field(name='<:gold:536793951571542016>\nHas gold?:', value=user_gold, inline=False)

                user.set_author(name="RedditBot", icon_url="https://i.redd.it/rq36kl1xjxr01.png")
                user.set_thumbnail(url=user_r.icon_img)
                user.set_footer(text="RedditBot " + version)
                await loadingMessage.edit(embed=user)

                # Update user info if changed
                if user_info["discord name"] != message.author.name:
                    user_info["discord name"] = message.author.name

                    with open("users/" + str(message.author.id) + '.json', 'w+') as outfile:
                        json.dump(user_info, outfile, indent=4)
        except FileNotFoundError:
            await loadingMessage.edit(message.author.mention + ' No connected account')

    if message.content.startswith('!connect'):
        user_name = message.content
        if message.content.__contains__('u/') == True:
            user_name = user_name.replace('!connect u/', '')
        else:
            user_name = user_name.replace('!connect ', '')

        user_r = reddit.redditor(user_name)

        code = 0
        code = code + random.randint(1000, 9999)

        data = {
            "registered": str(datetime.datetime.now()),
            "reddit name": user_name,
            "discord name": message.author.name,
            "discord id": message.author.id,
            "code": code,
            "connected": False,
            "has +": False
        }

        with open("users/" + str(message.author.id) + '.json', 'w+') as outfile:
            json.dump(data, outfile, indent=4)
        reddit.redditor(user_name).message('Discord user ' + data[
            "discord name"] + ' has tryed to connect to your discord account. Your code for Reddit',
                                           'This is your code: ' + str(
                                               code) + '\n\nIf you are being spammed by codes, dm me here: https://discord.gg/ZmyYxQg')
        await message.channel.send(
            message.author.mention + 'You have been sent a code on reddit. Do `!code [code]` to connect your account, if you have already have a connected account, it was removed')

    if message.content.startswith('!code'):
        users_code = message.content.replace('!code ', '')
        user_id = str(message.author.id)
        success = None
        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)
                if user_info["connected"] == True:
                    await message.channel.send(message.author.mention + " You already have a connected account!")
                    return
                elif str(user_info["code"]) == users_code:
                    success = True
        except FileNotFoundError:
            await message.channel.send(message.author.mention + " You haven't requested a code!")
            return
        if success == True:
            filename = "users/" + user_id + '.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                data['connected'] = True  # <--- add `id` value.
            os.remove(filename)
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            await message.channel.send(message.author.mention + " Done!")
        else:
            await message.channel.send(message.author.mention + " wrong code")

    if message.content.startswith('!unconnect'):
        user_id = str(message.author.id)
        try:
            os.remove("users/" + user_id + '.json')
            await message.channel.send("Done!")
        except FileNotFoundError:
            await message.channel.send(message.author.mention + " No pending to be or connected accounts")


@client.event
async def on_ready():
    print("Connected!")
    activity = discord.Game(name="!help | In " + str(len(client.guilds)) + " servers")
    print("Setting status to '" + str(activity) + "'")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)

client.run("NDM3NDM5NTYyMzg2NTA1NzMw.XS1p5g.Qnr00wIRIrc9EmK1ShlPCds1mWY")
