from discord.ext import commands
import discord, praw, datetime, json, os


version_number = "1.4.1"
version = version_number + " Created by bwac#2517"
red = 0xFF0000

with open("secrets.json") as json_file:
    secrets = json.load(json_file)

trophyemojis = None
with open("trophyemoji.json") as json_file:
    trophyemojis = json.load(json_file)

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True


class user(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ""

    @commands.command(name="user")
    async def user(self, ctx, username=None):
        """User command, r!user"""

        if username:
            loading = discord.Embed(title="", ncolor=red)
            loading.add_field(
                name="Loading...",
                value="<a:loading:650579775433474088> Contacting reddit servers...",
            )
            loading.set_footer(text="if it never loads, RedditBot can't find the user")
            loadingMessage = await ctx.send(embed=loading)

            reddit = praw.Reddit(
                client_id=secrets["reddit_id"],
                client_secret=secrets["reddit_secret"],
                user_agent="discord:n/a:" + version_number + " (by /u/-_-BWAC-_-)",
            )

            loading = discord.Embed(title="", color=red)
            loading.add_field(
                name="Loading...",
                value="<a:loading:650579775433474088> Getting profile info...",
            )
            loading.set_footer(
                text="if it never loads, something went wrong behind the scenes"
            )
            await loadingMessage.edit(embed=loading)

            time_cached = None
            name = None
            karma = None
            link_karma = None
            cake_day = None
            is_employee = None

            user_r = reddit.redditor(username)  # makes user

            if os.path.isfile("cache/users/" + username + ".json"):
                # If cache exists, read from it
                loading = discord.Embed(title="", color=red)
                loading.add_field(
                    name="Cache...",
                    value="<a:loading:650579775433474088> cache found! now loading from",
                )
                loading.set_footer(
                    text="if it never loads, something went wrong in the backround, or the username cant be found"
                )
                await loadingMessage.edit(embed=loading)
                with open("cache/users/" + username + ".json") as json_file:
                    cache = json.load(json_file)

                    time_cached = cache["time_cached"]
                    name = cache["name"]
                    karma = cache["karma"]
                    link_karma = cache["link_karma"]
                    cake_day = cache["cake_day"]
                    is_employee = cache["is_employee"]
            else:
                name = username
                karma = user_r.comment_karma
                link_karma = user_r.link_karma
                cake_day = datetime.datetime.fromtimestamp(
                    int(user_r.created)
                ).strftime("%m/%d/%Y")
                is_employee = user_r.is_employee

                cache = {
                    "time_cached": str(datetime.datetime.now()),
                    "name": name,
                    "karma": karma,
                    "link_karma": link_karma,
                    "cake_day": cake_day,
                    "is_employee": is_employee,
                }

                with open("cache/users/" + username + ".json", "w") as outfile:
                    json.dump(cache, outfile)

            user = discord.Embed(title="u/" + username + " info:", color=red)
            user.add_field(name="Karma:", value=karma)
            user.add_field(name="Link karma:", value=link_karma)
            user.add_field(name="All karma:", value=link_karma + karma)
            user.add_field(name="Cake Day:", value=cake_day)
            if time_cached:
                user.add_field(
                    name="*these results are from a cache made at*:",
                    value=time_cached,
                    inline=False,
                )
                user.add_field(
                    name="*if you want the latest stats, use r!resetuser "
                    + username
                    + "*",
                    value="keep in mind that you should only reset a user cache every so often",
                    inline=False,
                )

            trophiestxt = ""
            for trophy in user_r.trophies():
                emoji = ""
                if trophy.name in trophyemojis:
                    emoji = trophyemojis.get(trophy.name)
                if len(trophiestxt) > 900:
                    trophiestxt = (
                        trophiestxt
                        + "All the trophies are too long to send in a discord embed value so I "
                        "shortened them "
                    )
                    break
                trophiestxt = trophiestxt + emoji + trophy.name + "\n"
            user.add_field(name="Trophies:", value=trophiestxt)

            if is_employee:
                user.add_field(
                    name="This user", value="is an employee of reddit", inline=False
                )

            user.set_author(
                name="RedditBot",
                icon_url="https://images.discordapp.net/avatars/437439562386505730/2874f76dd780cb0af624e3049a6bfad0.png",
            )
            user.set_thumbnail(url=user_r.icon_img)
            user.set_footer(text="RedditBot " + version)
            await loadingMessage.edit(embed=user)
        else:
            error = discord.Embed(
                title="You didn't give a username!\n\nYou should use this command like:\nr!user `"
                "username`",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name="resetuser")
    async def resetuser(self, ctx, user_name=None):
        """resets a user cache"""

        if user_name:
            loading = discord.Embed(title="", color=red)
            loading.add_field(
                name="Deleting cache...", value="<a:loading:650579775433474088>"
            )
            loading.set_footer(text="if it never loads, RedditBot can't find the user")
            loadingMessage = await ctx.send(embed=loading)

            if os.path.isfile("cache/users/" + user_name + ".json"):
                os.remove("cache/users/" + user_name + ".json")

                loading = discord.Embed(title="", color=red)
                loading.add_field(
                    name="Deleted!...", value="now say r!user " + user_name
                )
                await loadingMessage.edit(embed=loading)
            else:
                loading = discord.Embed(title="", color=red)
                loading.add_field(
                    name="No cache!...", value="try saying r!user " + user_name
                )
                await loadingMessage.edit(embed=loading)
        else:
            error = discord.Embed(
                title="You didn't give a user name!\n\nYou should use this command like:\nr!resetuser `"
                "user name`",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(user(bot))
