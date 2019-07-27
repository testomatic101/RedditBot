import json
import os
import schedule
import discord
import praw

client = discord.Client()

reddit = praw.Reddit(client_id='HV16ttsYvjsrRw',
                     client_secret="StcBK-8Ml-VXM83xFFb0teO5ElM",
                     password='Redtrucke',
                     user_agent='reddit',
                     username='TheRedditBotDiscord')

version = '1.2.4'

red = 0xFF0000


def restart():
    import signal
    os.system("nohup python3 stream.py")
    os.kill(int(os.getpid()), signal.SIGKILL)


schedule.every(5).minutes.do(restart)

@client.event
async def on_ready():
    try:
        for submission in reddit.subreddit('all').stream.submissions():
            if os.path.exists('streams/' + str(submission.subreddit) + '.json'):
                with open('streams/' + str(submission.subreddit) + '.json') as sub_data:
                    sub_info = json.load(sub_data)
                    for channel_id in sub_info['channels']:
                        channel = client.get_channel(channel_id)
                        await channel.send('https://www.reddit.com/r/' + str(submission.subreddit) + '/comments/' + str(submission))
    except AttributeError:
        restart()

client.run('NDM3NDM5NTYyMzg2NTA1NzMw.XS7OkA.mCBMQDGVYXh-gpFps392AZrzjj0')
