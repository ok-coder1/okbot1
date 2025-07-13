from discord_http import Context, Client, commands, Member, PartialGuild
import os
from datetime import timedelta

client = Client(
    token = os.environ["DISCORD_BOT_TOKEN"],
    application_id = int(os.environ["DISCORD_APPLICATION_ID"]),
    public_key = os.environ["DISCORD_PUBLIC_KEY"],
    sync = True
)

'''
@client.command()
@commands.describe(
    message = "The message you want to send"
)
async def say(ctx, message: str):
    """ A command to send messages as the bot """
    return ctx.response.send_message(message)
'''

@client.command(user_install = True)
@commands.describe(
    user = "The user you want the avatar of"
)
async def avatar(ctx: Context, user: Member):
    """ Display the avatar of a user """
    return ctx.response.send_message("Here's the avatar of the user you requested. \n {}".format(str(user.display_avatar)))

@client.command()
@commands.describe(
    user = "The user you want to ban",
    reason = "The reason to ban"
)
async def ban(ctx: Context, user: Member, reason: str = None):
    """ Ban a user """
    guild = ctx.guild.fetch()
    await PartialGuild.ban(member = user, reason = reason)
    if reason is None:
        await user.send("You were banned in **`{}`**.".format(guild.name))
        return ctx.response.send_message("Successfully banned `{}`.".format(str(user)))
    else:
        await user.send("You were banned in **`{}`** for the following reason: **{}**.".format(guild.name, reason))
        return ctx.response.send_message("Successfully banned `{}` for **{}**.".format(str(user), reason))

@client.command()
@commands.describe(
    user = "The user ID you want to unban",
    reason = "The reason to unban"
)
async def unban(ctx: Context, user: Member, reason: str = None):
    """ Unban a user """
    guild = ctx.guild.fetch()
    await PartialGuild.unban(member = user, reason = reason)
    if reason is None:
        await user.send("You were unbanned in **`{}`**.".format(guild.name))
        return ctx.response.send_message("Successfully unbanned `{}`.".format(str(user)))
    else:
        await user.send("You werer unbanned in **`{}`** for the following reason: **{}**.".format(str(user), reason))


@client.command()
@commands.describe(
    user = "The user you want to mute",
    reason = "The reason you're muting this user",
    days = "The number of days to mute the user (type 0 if less than 1 day)",
    hours = "The number of hours to mute the user (type 0 if less than 1 hour)",
    minutes = "The number of minutes to mute the user (minimum has to be 1 if others are not filled)"
)
async def mute(ctx: Context, user: Member, days: int, hours: int, minutes: int, reason: str = None):
    """ Mute a user """
    guild = ctx.guild.fetch()
    muted_time = timedelta(days = days, hours = hours, minutes = minutes)
    await user.edit(communication_disabled_until = muted_time)
    await user.send("You were muted in **`{}`** for `{}` minutes for the following reason: **{}**.".format(guild.name, str(muted_time), reason))
    return ctx.response.send_message("Successfully muted `{}` for **{}**.".format(str(user), reason))

@client.command()
@commands.describe(
    user = "The user you want to unmute",
    reason = "The reason you're unmuting this user (leave blank if none)"
)
async def unmute(ctx: Context, user: Member):
    """ Unmute a user """
    guild = ctx.guild.fetch()
    await user.edit(communication_disabled_until = 0)
    await user.send("You were unmuted in **{}**.".format(guild.name))
    return ctx.response.send_message("Successfully unmuted `{}`".format(str(user)))

@client.command()
@commands.describe(
    user = "The user you want to kick",
    reason = "The reason you want to kick the user"
)
async def kick(ctx: Context, user: Member, reason: str = None):
    """ Kick a user """
    guild = ctx.guild.fetch()
    await user.send("You were kicked in **`{}`** for the following reason: **{}**.".format(guild.name, reason))
    await user.kick(reason = reason)
    return ctx.response.send_message("Successfully kicked `{}` for **{}**.".format(str(user), reason))

# TODO: Add back `/guildicon`
# Issue URL: https://github.com/ok-coder1/okbot1/issues/2
# assignees: ok-coder1
# labels: todo
'''
@client.command()
async def guildicon(ctx: Context):
    """ Icon of the guild """
    await Guild.fetch_guild()
    return ctx.response.send_message("Here's the icon of the guild." + "\n" + str(Guild.icon()))
'''

client.start()
