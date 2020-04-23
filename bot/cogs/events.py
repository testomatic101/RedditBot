from discord.ext import commands
import discord, praw, datetime, json, os, uuid


version_number = "1.4.2"
version = version_number + " Created by bwac#2517"
red = 0xFF0000
error_channel_id = 702452451231531029

# set if this is production or not
production = False
if os.path.isfile("production"):
    production = True

with open("secrets.json") as json_file:
    secrets = json.load(json_file)


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = ""

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready."""
        print("ready>")

        await self.bot.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game(
                name="r!help | In " + str(len(self.bot.guilds)) + " servers"
            ),
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.bot.change_presence(
            status=discord.Status.do_not_disturb,
            activity=discord.Game(
                name="r!help | In " + str(len(self.bot.guilds)) + " servers"
            ),
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Sends error to user and channel"""

        id = ""
        if production:
            id = "P"
        else:
            id = "B"
        id = id + str(uuid.uuid4().hex)
        print(type(error))
        # command not found
        if isinstance(error, commands.CommandNotFound):
            errorEmbed = discord.Embed(
                title=str(ctx.author) + " Command not found",
                description="[bug report](https://rbdis.xyz/bugreport)",
                color=red,
            )
            errorEmbed.set_footer(text=id + " " + version_number)
            await ctx.send(embed=errorEmbed)
            errorEmbed.add_field(
                name="error:", value=str(error) + "\n" + str(type(error)), inline=False,
            )
            await self.bot.get_channel(error_channel_id).send(embed=errorEmbed)
        # guild only
        elif isinstance(error, commands.NoPrivateMessage):
            errorEmbed = discord.Embed(
                title=str(ctx.author) + " Do this in a server", color=red,
            )
            errorEmbed.set_footer(text=id + " " + version_number)
            await ctx.send(embed=errorEmbed)
            errorEmbed.add_field(
                name="error:", value=str(error) + "\n" + str(type(error)), inline=False,
            )
            await self.bot.get_channel(error_channel_id).send(embed=errorEmbed)
        # cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            errorEmbed = discord.Embed(
                title=str(ctx.author) + " This command is on a cooldown",
                description="You can retry again in "
                + str(round(error.retry_after, 2))
                + "s",
                color=red,
            )
            errorEmbed.set_footer(text=id + " " + version_number)
            await ctx.send(embed=errorEmbed)
            errorEmbed.add_field(
                name="error:", value=str(error) + "\n" + str(type(error)), inline=False,
            )
            await self.bot.get_channel(error_channel_id).send(embed=errorEmbed)
        # sub not found
        elif (
            str(error)
            == "Command raised an exception: Redirect: Redirect to /subreddits/search"
            or str(error)
            == "Command raised an exception: NotFound: received 404 HTTP response"
        ):
            errorEmbed = discord.Embed(
                title=str(ctx.author) + " subreddit/user not found",
                description="Im not sure, but i think you entered a invalid sub/user\n[bug report](https://rbdis.xyz/bugreport)",
                color=red,
            )
            errorEmbed.set_footer(text=id + " " + version_number)
            await ctx.send(embed=errorEmbed)
            errorEmbed.add_field(
                name="error:", value=str(error) + "\n" + str(type(error)), inline=False,
            )
            await self.bot.get_channel(error_channel_id).send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(
                title=str(ctx.author) + " something went wrong",
                description="Im not sure what happened\n[Please report if this keeps happening](https://rbdis.xyz/bugreport)\n*`"
                + str(error)
                + "`*",
                color=red,
            )
            errorEmbed.set_footer(text=id + " " + version_number)
            await ctx.send(embed=errorEmbed)
            await self.bot.get_channel(error_channel_id).send(embed=errorEmbed)


def setup(bot):
    bot.add_cog(events(bot))
