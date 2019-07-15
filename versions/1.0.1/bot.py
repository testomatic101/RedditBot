#https://discordapp.com/api/oauth2/authorize?client_id=437439562386505730&permissions=8&scope=bot
import discord
import praw
import os
import random
import json

#from discord.ext import commands

client = discord.Client()

version = '1.0.1'

red = 0xFF0000

#reddit stuff
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     username='TheRedditBotDiscord',
                     password='',
                     user_agent='',)

#black list
black_list = ["gory", "watchpeopledie", "gore", "WPDtalk"]

class n:
    num = 10
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return


    if message.content.startswith('!help'):
        help = discord.Embed(title="Help:", description="**Welcome to the help page, here you can see all the commands TheRedditBot has to offer**\n\nPlease consider donating to help the development of this bot (This bot despratly needs a server upgrade) ", color=red)
        help.add_field(name="!help", value="Shows this page", inline=False)
        help.add_field(name="r/[sub name here]", value="Gives you some info on a subreddit", inline=False)
        help.add_field(name="u/[username here]", value="Gives you some info on a user", inline=False)
        help.add_field(name="!meme", value="Gives a random meme from /r/dankmemes on reddit!", inline=False)
        help.add_field(name="!me", value="See your account", inline=False)

        help_user = discord.Embed(title="User commands:", description="**Commands to add accounts and account management**", color=red)
        help_user.add_field(name="!connect u/[user name here]", value="Connect a reddit connect", inline=False)
        help_user.add_field(name="!unconnect", value="Unconnect the reddit account that you have connected", inline=False)
        help_user.add_field(name="!code", value="Submit the code you got from reddit", inline=False)

        help_user.set_footer(text="TheRedditBot " + version)
        await message.channel.send(embed=help)
        await message.channel.send(embed=help_user)



    if message.content.startswith('!meme'):
        random_post = reddit.subreddit('dankmemes').random()
        random_post_url = random_post.url
        await message.channel.send(random_post_url)

    if message.content.startswith('r/'):
        subreddit_name = message.content.replace("r/", "") #removes r/
        subreddit = reddit.subreddit(subreddit_name) #makes subreddit
        if subreddit.over18 == True:
            await message.channel.send(':underage: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:underage:')
            return
        if subreddit_name in black_list:
            await message.channel.send(f'Sorry {message.author.mention}, Due to discords tos (https://discordapp.com/terms) this bot can only show very limited content content')
            """To be worked on: time"""
            #created_on = subreddit.created_utc
            #created_on_date = time.strftime("%Y-%m-%d %H:%M:%S", created_on)

            sub=discord.Embed(title='**Cant show name due to discord tos** info:', color=red)
            sub.add_field(name='<:de:536791925727166484>\nDescription snippet:', value='**Cant show description due to discord tos**', inline=False)

            sub.add_field(name='<:su:536745418181312533>\nSubscriber Count:' , value=subreddit.subscribers, inline=False)

            '''To be worked on: time'''
            #sub.add_field(name='Created on:' , value=created_on_date, inline=False)

            sub.add_field(name='<:ns:536785325603946509>\nNSFW:' , value='No but is on the black list for subs that violate the tos', inline=False) #add variable here when i add channel nsfw checking
            sub.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
            sub.set_footer(text="TheRedditBot " + version)
            await message.channel.send(embed=sub)
        else:
            subreddit_description = subreddit.description
            subreddit_description = subreddit_description[:300]
            #subreddit_description = subreddit_description + '\n\n**To see the full description of** *' + subreddit_name + '* **use --full_description**'

            """To be worked on: time"""
            #created_on = subreddit.created_utc
            #created_on_date = time.strftime("%Y-%m-%d %H:%M:%S", created_on)

            sub=discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
            sub.add_field(name='<:de:536791925727166484>\nDescription snippet:', value=subreddit_description, inline=False)

            sub.add_field(name='<:su:536745418181312533>\nSubscriber Count:' , value=subreddit.subscribers, inline=False)

            '''To be worked on: time'''
            #sub.add_field(name='Created on:' , value=created_on_date, inline=False)

            sub.add_field(name='<:ns:536785325603946509>\nNSFW:' , value='No', inline=False) #add variable here when i add channel nsfw checking
            sub.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
            sub.set_thumbnail(url=subreddit.icon_img)
            sub.set_footer(text="TheRedditBot " + version)
            await message.channel.send(embed=sub)

    if message.content.startswith('u/'):
        user_name = message.content.replace("u/", "") #removes u/
        user_r = reddit.redditor(user_name) #makes user

        '''to be worked on, is gold?'''
        #user_gold = ''
        #if user_r.is_gold == False:
            #user_gold == 'No'
        #else:
            #user_gold == 'yes'
        user=discord.Embed(title='u/' + user_r.name + ' info:', color=red)
        user.add_field(name='<:karma:536792660057391104>\nKarma:', value=user_r.comment_karma, inline=False)
        user.add_field(name='<:link_karma:536793553238491166>\nLink karma:', value=user_r.link_karma, inline=False)
        #user.add_field(name='<:gold:536793951571542016>\nHas gold?:', value=user_gold, inline=False)

        user.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
        user.set_thumbnail(url=user_r.icon_img)
        user.set_footer(text="TheRedditBot " + version)
        await message.channel.send(embed=user)

    if message.content.startswith('!me'):
        user_id = str(message.author.id)


        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)
        except FileNotFoundError:
            await message.channel.send(f'{message.author.mention} No connected account')

        if user_info["connected"] == False:
            await message.channel.send(f'{message.author.mention} No connected account')
            return

        user_name = str(user_info["user name"])

        user_r = reddit.redditor(user_name) #makes user

        #to be worked on, is gold?
        #user_gold = ''
        #if user_r.is_gold == False:
            #user_gold == 'No'
        #else:
            #user_gold == 'yes'


        user=discord.Embed(title='u/' + user_r.name + ' info:', color=red)
        user.add_field(name='<:karma:536792660057391104>\nKarma:', value=user_r.comment_karma, inline=False)
        user.add_field(name='<:link_karma:536793553238491166>\nLink karma:', value=user_r.link_karma, inline=False)
        #user.add_field(name='<:gold:536793951571542016>\nHas gold?:', value=user_gold, inline=False)

        user.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
        user.set_thumbnail(url=user_r.icon_img)
        user.set_footer(text="TheRedditBot " + version)
        await message.channel.send(embed=user)


        await message.channel.send(f'{message.author.mention} Your connected account is ' + user_name)


    if message.content.startswith('!connect'):
        user_name = message.content
        if message.content.__contains__('u/') == True:
            user_name = user_name.replace('!connect u/', '')
        else:
            user_name = user_name.replace('!connect ', '')

        user_r = reddit.redditor(user_name)

        code = 0
        code = code + random.randint(1000,9999)

        data = {
          "user name": user_name,
          "code": code,
          "connected": False
        }

        with open("users/" + str(message.author.id) + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        reddit.redditor(user_name).message('Your code for TheRedditBot', 'This is your code: ' + str(code) + '\n\nIf you are being spamed by codes, dm me here: https://bwac.pro/trb')
        await message.channel.send(f'{message.author.mention} You have been sent a code on reddit. Do `!code [code]` to connect your account, if you have already have a connected account, it was removed')

    if message.content.startswith('!code'):
        users_code = message.content.replace('!code ', '')
        user_id = str(message.author.id)
        success = None
        try:
            with open("users/" + user_id + '.json') as user_data:
                user_info = json.load(user_data)
                if user_info["connected"] == True:
                    await message.channel.send(f"{message.author.mention} You already have a connected account!")
                    return
                elif str(user_info["code"]) == users_code:
                    success = True
        except FileNotFoundError:
            await message.channel.send(f"{message.author.mention} You havent requested a code!")
            return
        if success == True:
            filename = "users/" + user_id + '.json'
            with open(filename, 'r') as f:
                data = json.load(f)
                data['connected'] = True # <--- add `id` value.
            os.remove(filename)
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            await message.channel.send(f"{message.author.mention} Done!")
        else:
            await message.channel.send(f"{message.author.mention} wrong code")


    if message.content.startswith('!unconnect'):
        user_id = str(message.author.id)
        try:
            os.remove("users/" + user_id + '.json')
            await message.channel.send("Done!")
        except FileNotFoundError:
            await message.channel.send(f"{message.author.mention} No pending to be or connected accounts")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('client version=' + version)

client.run('') #main
#client.run('') #beta


'''
Todos:

make encryption for code(not done)


'''