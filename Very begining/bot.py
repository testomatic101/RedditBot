#https://discordapp.com/api/oauth2/authorize?client_id=437439562386505730&permissions=8&scope=bot
import discord
import random
import praw

#reddit stuff



@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
    
    if message.content.startswith('!meme'):
        random_post = reddit.subreddit('dankmemes').random()
        random_post_url = random_post.url
        await message.channel.send(random_post_url)
        
    if message.content.startswith('!help'):
        embed = discord.Embed(title="Help:", description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=False)
        embed.add_field(name="Field2", value="hi2", inline=False)
        await client.send_message(message.channel, embed=embed)
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client = MyClient()
client.run('token')
