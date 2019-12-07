import discord
from discord.ext import commands
import praw
import random
import datetime
import json
import os

version = '1.2.4 (patch 5) Created by bwac#2517'
red = 0xFF0000

trophyEmojis = {
    "Bellwether": "<:bellwether:651535357837443093>",
    "Well-rounded": "<:wellrounded:651535373360431124>",
    "Best Link": "<:bestlink:651535358546411530>",
    "Best Comment": "<:bestcomment:651535357850025995> ",
    "ComboLinker": "<:combolinker:651535362744647692>",
    "ComboCommenter": "<:combocommenter:651535362489057280>",
    "Inciteful Link": "<:incitefullink:651535363835428892>",
    "Inciteful Comment": "<:incitefulcomment:651535363843817503> ",
    "Shutterbug": "<:shutterbug:651535366851133490> ",
    "New User": "<:newuser:651535365244452874>",
    "Verified Email": "<:verifiedemailaddress:651535373113098241> ",
    "Gilding": "<:gilding:651535364087087114>",
    "One-Year Club": "<:oneyearclub:651535365290721310>",
    "Two-Year Club": "<:twoyearclub:651535373104578584>",
    "Three-Year Club": "<:threeyearclub:651535372861440011>",
    "Four-Year Club": "<:fouryearclub:651535363617325077>",
    "Five-Year Club": "<:fiveyearclub:651535363210346527> ",
    "Six-Year Club": "<:sixyearclub:651535366817447936>",
    "Seven-Year Club": "<:sevenyearclub:651535366377046036>",
    "Eight-Year Club": "<:eightyearclub:651535362799435836>",
    "Nine-Year Club": "<:nineyearclub:651535365294784512> ",
    "Ten-Year Club": "<:tenyearclub:651535372223905799> ",
    "Eleven-Year Club": "<:elevenyearclub:651535363688497180>",
    "Twelve-Year Club": "<:twelveyearclub:651535373255573528>",
    "Thirteen-Year Club": "<:thirteenyearclub:651535373217955864>",
    "Translator": "<:translator:651535372882542602> ",
    "Open Sorcerer": "<:opensorcerer:651535365597036575>",
    "White Hat": "<:whitehat:651535373276807168>",
    "CSS Animal": "<:cssanimal:651535362778202115> ",
    "Artisan": "<:artisan:651535357640310804>",
    "Beta Team": "<:betateam:651535358642880512>",
    "Reddit Premium": "<:redditgold:651535365957484573> ",
    "Reddit Mold": "<:moldparticipant:651655524265361418>",
    "Charter Member": "<:chartermember:651535358927962132> ",
    "Alienator": "<:alienator:651535357489315870>",
    "Team Orangered": "<:teamorangered:651535372613844992>",
    "Team Periwinkle": "<:teamperiwinkle:651535372697731102>",
    "Spared": "<:spared:651535372609912835> ",
    "Snapped": "<:snapped:651535371724783627>",
    "Not Forgotten": "<:not_forgotten:651653586450776074>",
    "14-Year Club": "<:14_year_club:651653962117677056>",
    "RPAN Viewer": "<:rpanviewer:651654358378741761>",
    "Sequence | Editor": "<:sequence_editor:651654554588545074>",
    "Alpha Tester": "<:alpha_user:651654781005332499>",
    "redditgifts Exchanges": "<:rgexchange:651655033477398539>",
    "redditgifts Elf": "<:rgiftself:651655190642032643>",
    "Rally Monkey": "<:represent:651655848086470666>"
}


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
                                              code) + '\n\nIf you are being spammed by codes, dm me here: '
                                                      'https://discord.gg/ZmyYxQg')
        await ctx.author.send('You have been sent a code on reddit. Do `rcode [code]` to connect your account, '
                              'if you have already have a connected account, it was removed')

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
                if user_info["connected"]:
                    await ctx.channel.send(ctx.author.mention + " You already have a connected account!")
                    return
                elif str(user_info["code"]) == code:
                    success = True
        except FileNotFoundError:
            await ctx.channel.send(ctx.author.mention + " You haven't requested a code!")
            return
        if success:
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
                loading.add_field(name='Loading...',
                                  value='<a:loading:650579775433474088> Contacting reddit servers...')
                loading.set_footer(text="if it never loads, something is probably wrong with your connected account. "
                                        "Try !unconnect then reconnect then try again")
                await loadingMessage.edit(embed=loading)

                reddit = praw.Reddit(client_id='MYX2-K7jabb3LA',
                                     client_secret='gy6XLBwv_AcRcUZm_fN6Ef-n0Hs',
                                     user_agent='redditbot')

                loading = discord.Embed(title='', color=red)
                loading.add_field(name='Loading...',
                                  value='<a:loading:650579775433474088> Getting your profile info...')
                loading.set_footer(text="if it never loads, something went wrong behind the scenes")
                await loadingMessage.edit(embed=loading)

                user_r = reddit.redditor(user_info['reddit name'])  # makes user
                if not user_info["connected"]:
                    await ctx.channel.send(ctx.author.mention + ' No connected account')
                    return

                user = discord.Embed(title='u/' + user_r.name + ' info:', color=red)
                user.add_field(name='Karma:', value=user_r.comment_karma)
                user.add_field(name='Link karma:', value=user_r.link_karma)
                user.add_field(name='All karma:', value=user_r.link_karma + user_r.comment_karma)
                user.add_field(name='Cake Day:',
                               value=datetime.datetime.fromtimestamp(int(user_r.created)).strftime('%m/%d/%Y'),
                               inline=False)
                trophiestxt = ''
                for trophy in user_r.trophies():
                    emoji = ''
                    if trophy.name in trophyEmojis:
                        emoji = trophyEmojis.get(trophy.name)
                    if len(trophiestxt) > 950:
                        trophiestxt = trophiestxt + 'All the trophies are too long to send in a discord embed value'
                        break
                    trophiestxt = trophiestxt + emoji + trophy.name + '\n'
                user.add_field(name='Trophies:', value=trophiestxt)

                if user_r.is_employee:
                    user.add_field(name='You are', value='an employee of reddit!')

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
