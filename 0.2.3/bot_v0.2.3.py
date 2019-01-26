##https://discordapp.com/api/oauth2/authorize?client_id=437439562386505730&permissions=8&scope=bot
import discord
import praw
from discord.ext import commands
import os
import time

client = discord.Client()

version = '0.2.3'

red = 0xFF0000

#reddit stuff



@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        help = discord.Embed(title="Help:", description="**Version = " + version + "**\nWelcome to the help page, here you can see all the commands TheRedditBot has to offer", color=red)
        help.add_field(name="!help", value="Shows this page", inline=False)
        help.add_field(name="r/[sub name here]", value="Gives you some info on a subreddit", inline=False)
        help.add_field(name="u/[username here]", value="Gives you some info on a user", inline=False)

        #help.add_field(name="!full_description r/[sub name here]", value="Gives the full description of a subreddit", inline=False)
        #help.add_field(name="!icon r/[sub name here]", value="Gives the subreddit icon only", inline=False)
        #help.add_field(name="!subscribers r/[sub name here]", value="Gives the subscriber count of a subreddit", inline=False)
        help.add_field(name="!meme", value="Gives a random meme from /r/dankmemes on reddit!", inline=False)
        help.set_footer(text="TheRedditBot " + version)
        await message.channel.send(embed=help)


    if message.content.startswith('!meme'):
        random_post = reddit.subreddit('dankmemes').random()
        random_post_url = random_post.url
        await message.channel.send(random_post_url)

    if message.content.startswith('r/'):
        subreddit_name = message.content.replace("r/", "") #removes r/
        subreddit = reddit.subreddit(subreddit_name) #makes subreddit

        subreddit_description = subreddit.description

        subreddit_description = subreddit_description[:300]
        #subreddit_description = subreddit_description + '\n\n**To see the full description of** *' + subreddit_name + '* **use --full_description**'

        """To be worked on: time"""
        #created_on = subreddit.created_utc
        #created_on_date = time.strftime("%Y-%m-%d %H:%M:%S", created_on)

        if subreddit.over18 == True:
            await message.channel.send(':underage: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:underage:')
            return
        sub=discord.Embed(title='r/' + subreddit_name + ' info:', color=red)
        sub.add_field(name='<:de:536791925727166484>\nDescription snippet:', value=subreddit_description + '\n\n**To see the full description use --full_description**', inline=False)

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
        user_gold = ''
        if user_r.is_gold == False:
            user_gold = 'No'
        else:
            user_gold = 'yes'
        user=discord.Embed(title='u/' + user_r.name + ' info:', color=red)
        user.add_field(name='<:karma:536792660057391104>\nKarma:', value=user_r.comment_karma, inline=False)
        user.add_field(name='<:link_karma:536793553238491166>\nLink karma:', value=user_r.link_karma, inline=False)
        user.add_field(name='<:gold:536793951571542016>\nHas gold?:', value=user_gold, inline=False)

        user.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
        user.set_thumbnail(url=user_r.icon_img)
        user.set_footer(text="TheRedditBot " + version)
        await message.channel.send(embed=user)


#    if message.content.startswith('!full_description'):
#        subreddit_name = message.content.replace("--full_description r/", "") #removes r/
#        subreddit = reddit.subreddit(subreddit_name) #makes subreddit
#        subreddit_description = subreddit.description
#        subreddit_description = subreddit_description[:1900]
#
#        if subreddit.over18 == True:
#            await message.channel.send(':x: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:x:')
#            return
#        sub=discord.Embed(title='r/' + subreddit_name + "'s full description:", description=subreddit_description, color=red)
#        sub.set_author(name="TheRedditBot",icon_url="https://i.redd.it/rq36kl1xjxr01.png")
#        sub.set_thumbnail(url=subreddit.icon_img)
#        sub.set_footer(text="TheRedditBot")
#        await message.channel.send(embed=sub)
#
#    if message.content.startswith('!icon'):
#        subreddit_name = message.content.replace("--icon r/", "") #removes r/
#        subreddit = reddit.subreddit(subreddit_name) #makes subreddit
#        if subreddit.over18 == True:
#            await message.channel.send(':x: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:x:')
#            return
#        await message.channel.send(subreddit.icon_img)
#
#    if message.content.startswith('!subscribers'):
#        subreddit_name = message.content.replace("--icon r/", "") #removes r/
#        subreddit = reddit.subreddit(subreddit_name) #makes subreddit
#        if subreddit.over18 == True:
#            await message.channel.send(':x: this is subreddit has been marked as nsfw! If you really what to see that, go to reddit your self!:x:')
#            return
#
#        await message.channel.send(f'{subreddit} has {subreddit.subscribers}')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('client version=' + version)

client.run('') #main
#client.run('') #beta
