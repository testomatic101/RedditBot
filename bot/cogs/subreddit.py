from discord.ext import commands
import discord, praw, datetime, json, os, math, wget, uuid
from PIL import Image, ImageDraw, ImageFont, ImageOps
from textwrap import wrap

version_number = "1.4"
version = version_number + " Created by bwac#2517"
red = 0xFF0000

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True

with open("secrets.json") as json_file:
    secrets = json.load(json_file)


class subreddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ""

    @commands.command(name="subreddit")
    async def subreddit(self, ctx, subreddit_name=None):
        """Subreddit command, r!subreddit"""

        if subreddit_name:
            if ctx.guild:
                reddit = praw.Reddit(
                    client_id=secrets["reddit_id"],
                    client_secret=secrets["reddit_secret"],
                    user_agent="discord:n/a:" + version_number + " (by /u/-_-BWAC-_-)",
                )

                id = str(uuid.uuid4().hex)

                subreddit = reddit.subreddit(subreddit_name)
                if ctx.channel.is_nsfw():
                    loadingMessage = await ctx.send("<a:loading:650579775433474088>")

                    time_cached = None
                    time_created = None
                    display_name = None
                    name = None
                    smalldes = None
                    subcount = None
                    nsfw = None
                    thumbnail = None

                    if os.path.isfile("cache/subreddits/" + subreddit_name + ".json"):
                        # If cache exists, read from it
                        with open(
                            "cache/subreddits/" + subreddit_name + ".json"
                        ) as json_file:
                            cache = json.load(json_file)

                            time_cached = cache["time_cached"]
                            time_created = cache["time_created"]
                            display_name = cache["display_name"]
                            smalldes = cache["smalldes"]
                            subcount = cache["subcount"]
                            nsfw = cache["nsfw"]
                            thumbnail = cache["thumbnail"]
                    else:
                        # If cache doesnt exit, make it
                        try:
                            smalldes = subreddit.public_description
                        except:
                            smalldes = None
                        time_created = subreddit.created_utc
                        display_name = subreddit.display_name
                        subcount = subreddit.subscribers
                        nsfw = subreddit.over18
                        thumbnail = subreddit.icon_img

                        cache = {
                            "time_cached": str(datetime.datetime.now()),
                            "time_created": time_created,
                            "display_name": display_name,
                            "smalldes": smalldes,
                            "subcount": subcount,
                            "nsfw": nsfw,
                            "thumbnail": thumbnail,
                        }
                        with open(
                            "cache/subreddits/" + subreddit_name + ".json", "w"
                        ) as outfile:
                            json.dump(cache, outfile)

                    time_created = datetime.datetime.fromtimestamp(
                        time_created
                    ).strftime("%m/%d/%Y")

                    millnames = ["", "K", "M", "B", "T"]

                    n = float(subcount)
                    millidx = max(
                        0,
                        min(
                            len(millnames) - 1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3)),
                        ),
                    )

                    new_subcount = "{:.0f}{}".format(
                        n / 10 ** (3 * millidx), millnames[millidx]
                    )

                    """Imaging"""
                    im = Image.open("images/subreddit.png")
                    draw = ImageDraw.Draw(im)
                    normal_font = ImageFont.truetype("OpenSans-Regular.ttf", size=14)
                    small_font = ImageFont.truetype("OpenSans-Regular.ttf", size=7)

                    wrapped_text = wrap(smalldes, 40)
                    if len(wrapped_text) > 5:
                        wrapped_text = wrapped_text[:5]
                        wrapped_text[len(wrapped_text) - 1] = (
                            wrapped_text[len(wrapped_text) - 1] + "(...)"
                        )
                    wrapped_text = "\n".join(wrapped_text)

                    draw.text(
                        (12, 120),
                        text=wrapped_text,
                        fill=(255, 255, 255),
                        font=normal_font,
                    )
                    draw.text(
                        (12, 225),
                        text=new_subcount,
                        fill=(255, 255, 255),
                        font=normal_font,
                    )
                    draw.text(
                        (90, 290),
                        text=time_created,
                        fill=(255, 255, 255),
                        font=normal_font,
                    )
                    if nsfw:
                        draw.text(
                            (140, 225),
                            text="Yes",
                            fill=(255, 255, 255),
                            font=normal_font,
                        )
                    else:
                        draw.text(
                            (140, 225),
                            text="No",
                            fill=(255, 255, 255),
                            font=normal_font,
                        )
                    draw.text(
                        (135, 35),
                        text=display_name,
                        fill=(255, 255, 255),
                        font=normal_font,
                    )
                    draw.text(
                        (135, 53),
                        text="r/" + subreddit_name,
                        fill=(214, 214, 214),
                        font=normal_font,
                    )

                    # make thumbnail a circle
                    if not subreddit.icon_img == "":
                        local_image_filename = wget.download(
                            subreddit.icon_img, "temp/thumb" + id + ".png"
                        )
                        im_thumb = Image.open(local_image_filename)
                        im_thumb = im_thumb.resize((60, 60))
                        mask = Image.open("images/mask.png")
                        im_thumb.paste(mask, (0, 0), mask)
                        im.paste(im_thumb, (70, 25))
                    im.save("temp/re" + id + ".png")

                    if time_cached:
                        await ctx.send(
                            "this was chached at "
                            + time_cached
                            + " (r!resetsub "
                            + subreddit_name
                            + " to get latest stats)",
                            file=discord.File("temp/re" + id + ".png"),
                        )
                        await bot.get_channel(700277796148215838).send(
                            "this was chached at "
                            + time_cached
                            + " (r!resetsub "
                            + subreddit_name
                            + " to get latest stats)",
                            file=discord.File("temp/re" + id + ".png"),
                        )
                    else:
                        await ctx.send(file=discord.File("temp/re" + id + ".png"))
                        await bot.get_channel(700277796148215838).send(
                            file=discord.File("temp/re" + id + ".png")
                        )
                    await loadingMessage.delete()

                    os.remove("temp/re" + id + ".png")
                    os.remove(local_image_filename)
                else:
                    error = discord.Embed(title="Error", color=red)
                    error.add_field(
                        name="Sorry",
                        value="The channel **"
                        + ctx.channel.name
                        + "** is not nsfw, to be safe "
                        "with the discord tos and "
                        "such, you will have to "
                        "change the channel to nsfw.",
                    )
                    await loadingMessage.edit(embed=error)
            else:
                await ctx.send("Please do this in a server")
        else:
            error = discord.Embed(
                title="You didn't give a subreddit!\n\nYou should use this command like:\nr!subreddit ["
                "subreddit name]",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name="top")
    async def top(self, ctx, subreddit_name=None):
        """get the top posts of a subreddit, rtop"""

        loading = discord.Embed(title="", color=red)
        loading.add_field(
            name="Loading...",
            value="<a:loading:650579775433474088> Contacting reddit " "servers...",
        )
        loading.set_footer(
            text="if it never loads, RedditBot can't find the subreddit, or something broke"
        )
        loadingMessage = await ctx.send(embed=loading)

        if subreddit_name:
            if ctx.channel.is_nsfw():
                reddit = praw.Reddit(
                    client_id=secrets["reddit_id"],
                    client_secret=secrets["reddit_secret"],
                    user_agent="discord:n/a:" + version_number + " (by /u/-_-BWAC-_-)",
                )

                embed = discord.Embed(
                    title="r/" + subreddit_name + "'s top 10 top posts as of right now",
                    description="",
                    color=red,
                )

                for submission in reddit.subreddit(subreddit_name).top(limit=10):
                    if len(embed) < 6000:
                        embed.description = (
                            embed.description
                            + "\n\n["
                            + submission.title
                            + "](https://reddit.com"
                            + submission.permalink
                            + ")\n:thumbsup:"
                            + str(submission.score)
                            + ", u/"
                            + str(submission.author)
                            + ", "
                            + str(
                                datetime.datetime.fromtimestamp(
                                    submission.created_utc
                                ).strftime("%m/%d/%Y")
                            )
                        )
                        await loadingMessage.edit(embed=embed)
            else:
                error = discord.Embed(title="Error", color=red)
                error.add_field(
                    name="Sorry",
                    value="The channel **"
                    + ctx.channel.name
                    + "** is not nsfw, to be safe "
                    "with the discord tos and "
                    "such, you will have to "
                    "change the channel to nsfw.",
                )
                await loadingMessage.edit(embed=error)
        else:
            error = discord.Embed(
                title="You didn't give a subreddit!\n\nYou should use this command like:\nr!top ["
                "subreddit name]",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name="hot")
    async def hot(self, ctx, subreddit_name=None):
        """get the current hot posts of a subreddit, r!hot"""

        loading = discord.Embed(title="", color=red)
        loading.add_field(
            name="Loading...",
            value="<a:loading:650579775433474088> Contacting reddit " "servers...",
        )
        loading.set_footer(
            text="if it never loads, RedditBot can't find the subreddit, or something broke"
        )
        loadingMessage = await ctx.send(embed=loading)

        if subreddit_name:
            if ctx.channel.is_nsfw():
                reddit = praw.Reddit(
                    client_id=secrets["reddit_id"],
                    client_secret=secrets["reddit_secret"],
                    user_agent="discord:n/a:" + version_number + " (by /u/-_-BWAC-_-)",
                )

                embed = discord.Embed(
                    title="r/" + subreddit_name + "'s top 10 hot posts as of right now",
                    description="",
                    color=red,
                )
                for submission in reddit.subreddit(subreddit_name).hot(limit=10):
                    if len(embed) < 6000:
                        embed.description = (
                            embed.description
                            + "\n\n["
                            + submission.title
                            + "](https://reddit.com"
                            + submission.permalink
                            + ")\n:thumbsup:"
                            + str(submission.score)
                            + ", u/"
                            + str(submission.author)
                            + ", "
                            + str(
                                datetime.datetime.fromtimestamp(
                                    submission.created_utc
                                ).strftime("%m/%d/%Y")
                            )
                        )
                    await loadingMessage.edit(embed=embed)
            else:
                error = discord.Embed(title="Error", color=red)
                error.add_field(
                    name="Sorry",
                    value="The channel **"
                    + ctx.channel.name
                    + "** is not nsfw, to be safe "
                    "with the discord tos and "
                    "such, you will have to "
                    "change the channel to nsfw.",
                )
                await loadingMessage.edit(embed=error)
        else:
            error = discord.Embed(
                title="You didn't give a subreddit!\n\nYou should use this command like:\nr!hot ["
                "subreddit name]",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)

    @commands.command(name="resetsub")
    async def resetsub(self, ctx, subreddit_name=None):
        """resets a subreddit cache"""

        if subreddit_name:
            loading = discord.Embed(title="", color=red)
            loading.add_field(
                name="Deleting cache...", value="<a:loading:650579775433474088>"
            )
            loading.set_footer(
                text="if it never loads, RedditBot can't find the subreddit"
            )
            loadingMessage = await ctx.send(embed=loading)

            if os.path.isfile("cache/subreddits/" + subreddit_name + ".json"):
                os.remove("cache/subreddits/" + subreddit_name + ".json")

                loading = discord.Embed(title="", color=red)
                loading.add_field(
                    name="Deleted!...", value="now say r!subreddit " + subreddit_name
                )
                await loadingMessage.edit(embed=loading)
            else:
                loading = discord.Embed(title="", color=red)
                loading.add_field(
                    name="No cache!...",
                    value="try saying r!subreddit " + subreddit_name,
                )
                await loadingMessage.edit(embed=loading)
        else:
            error = discord.Embed(
                title="You didn't give a subreddit!\n\nYou should use this command like:\nr!resetsub ["
                "subreddit name]",
                color=red,
            )
            error.set_footer(text=version)
            await ctx.send(embed=error)


def setup(bot):
    bot.add_cog(subreddit(bot))
