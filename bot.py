import discord
from discord.ext import commands
from settings import Settings
import statistics
import embed_creator
import json
import os
from decouple import config
import time
import threading



def determine_prefixes(bot, message):
    return settings.get_prefix(message.guild.id)

settings = Settings()
client = discord.Client()
bot = commands.Bot(command_prefix=determine_prefixes)
bot.remove_command('help')

#################### SETTINGS ####################

@bot.command()
async def setprefix(ctx, *args):
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 1):
            prefix = await bot.get_prefix(ctx.message)
            await ctx.send("**Invalid command!** Correct usage: `" + prefix + "setprefix {newprefix}`.")
            return False
        else:
            await settings.set_prefix(ctx.message.guild.id, args[0])
            prefix = await bot.get_prefix(ctx.message)
            await ctx.send(":white_check_mark: Prefix set to **" + prefix + "**")


#################### COMMANDS ####################

async def is_disabled(ctx):
    admin = ctx.message.author.guild_permissions.administrator
    disabled = await settings.check_disabled_channel(ctx.message.guild.id, ctx.message.channel.id)
    return not disabled or admin

@bot.command()
@commands.check(is_disabled)
async def help(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    user_help_string = ":grey_question: HyperStats Help :grey_question:\n\n Prefix: `" + prefix + "`"
    if ctx.message.author.guild_permissions.administrator: 
        user_help_string += "\n\n`" + prefix + "setprefix {prefix}`: Changes the bot prefix **(admin only)**."
        user_help_string += "\n`" + prefix + "disablechannel`: Disables the bot in the channel this command is used in for non-administrators **(admin only)**."
        user_help_string += "\n`" + prefix + "enablechannel`: Enables the bot in the channel this command is used in for non-administrators **(admin only)**."
        user_help_string += "\n`" + prefix + "listdisabledchannels`: Lists all disabled channels **(admin only)**."
    user_help_string += "\n\n`" + prefix + "help`: Displays this menu."
    user_help_string += "\n`" + prefix + "about`: Displays information about this bot."
    user_help_string += "\n`" + prefix + "link {playername} {platform}`: Links your discord account to your in-game account. Once complete, you can use the below commands without any arguments to view your own stats."
    user_help_string += "\n`" + prefix + "unlink`: Unlinks your in-game account from your discord account."
    user_help_string += "\n\nFor all of the below commands, platform must be either be empty for PC, or one of `PC`, `Xbox` or `PS`. You can also use `" + prefix + "link {playername} {platform}` to use the below commands to view your own stats without any arguments."
    user_help_string += "\n\n`" + prefix + "stats {playername} {platform}`: Displays player stats."
    user_help_string += "\n`" + prefix + "weapons {playername} {platform}`: Displays weapon stats for a player."
    user_help_string += "\n`" + prefix + "hacks {playername} {platform}`: Displays hack stats for a player."
    user_help_string += "\n`" + prefix + "best {playername} {platform}`: Displays career best stats for a player (best in one game)."
    await ctx.send(user_help_string)


@bot.command()
@commands.check(is_disabled)
async def stats(ctx, *args):
    await api_down(ctx)
    linked = await statistics.is_linked(settings, ctx, args, "stats")
    if linked:
        return
    valid = await check_stats_commands(ctx, "stats", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await statistics.determine_platform(status, args)
        await statistics.show_statistics(ctx, status, "stats", args[0], platform)


@bot.command()
@commands.check(is_disabled)
async def weapons(ctx, *args):
    await api_down(ctx)
    linked = await statistics.is_linked(settings, ctx, args, "weapons")
    if linked:
        return
    valid = await check_stats_commands(ctx, "weapons", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await statistics.determine_platform(status, args)
        await statistics.show_statistics(ctx, status, "weapons", args[0], platform)


@bot.command()
@commands.check(is_disabled)
async def best(ctx, *args):
    await api_down(ctx)
    linked = await statistics.is_linked(settings, ctx, args, "best")
    if linked:
        return
    valid = await check_stats_commands(ctx, "best", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await statistics.determine_platform(status, args)
        await statistics.show_statistics(ctx, status, "best", args[0], platform)

@bot.command()
@commands.check(is_disabled)
async def hacks(ctx, *args):
    await api_down(ctx)
    linked = await statistics.is_linked(settings, ctx, args, "hacks")
    if linked:
        return
    valid = await check_stats_commands(ctx, "hacks", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await statistics.determine_platform(status, args)
        await statistics.show_statistics(ctx, status, "hacks", args[0], platform)

@bot.command()
async def disablechannel(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 0):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "disablechannel`. Use this command in the channel you'd like to disable the bot in!")
        else:
            disable = await settings.disable_channel(ctx.message.guild.id, ctx.message.channel.id)
            if disable:
                await ctx.send(":white_check_mark: Bot **disabled** in channel for non-administrators.")
            else:
                await ctx.send(":stop_sign: Bot **already disabled** in channel.")

@bot.command()
@commands.check(is_disabled)
async def about(ctx, *args):
    embed = await embed_creator.create_about_embed()
    await ctx.send(embed=embed)


@bot.command()
async def enablechannel(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 0):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "enablechannel`. Use this command in the channel you'd like to enable the bot in!")
        else:
            enable = await settings.enable_channel(ctx.message.guild.id, ctx.message.channel.id)
            if enable:
                await ctx.send(":white_check_mark: Bot **enabled** in channel for non-administrators.")
            else:
                await ctx.send(":stop_sign: Bot **already enabled** in channel.")

@bot.command()
async def listdisabledchannels(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 0):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "listdisabledchannels`.")
        else:
            await ctx.send(await settings.get_disabled_channels(ctx.message.guild.id))

@bot.command()
@commands.check(is_disabled)
async def link(ctx, *args):
    await api_down(ctx)
    prefix = await bot.get_prefix(ctx.message)
    already_linked = await settings.get_linked_user(ctx.message.author.id)
    if already_linked is not None:
        await ctx.send(":stop_sign: This account is already linked to **" + already_linked['p_name'] + "**!")
        return False
    if (len(args) != 2 and len(args) != 1):
        await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "link {playername} {platform}`. Platform must either be `PC`, `Xbox` or `PS` (or blank for PC).")
        return False
    status = await ctx.send(":hourglass: Attempting to link player " + args[0] + "...")
    platform = await statistics.determine_platform(status, args)
    id = await statistics.find_player(status, args[0], platform)
    if not id:
        await status.edit(content=":exclamation: Failed to find player **" + args[0] + "**! Link failed!")
    else:
        await settings.add_link(ctx.message.author.id, id["p_id"], id["p_name"], id['p_platform'])
        await status.edit(content=":white_check_mark: Your Discord account has been linked to **" + id["p_name"] + "**! You can now use the commands without the extra parameters!")

@bot.command()
@commands.check(is_disabled)
async def unlink(ctx, *args):
    already_linked = await settings.get_linked_user(ctx.message.author.id)
    if already_linked is not None:
        await ctx.send(":stop_sign: Unlinked **" + already_linked['p_name'] + "** from your discord account!")
        await settings.remove_link(ctx.message.author.id)
        return True
    else:
        await ctx.send(":stop_sign: No account linked!")
        return False

#################### HELPER ####################

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" " + str(len(bot.guilds)) + " servers | $help"))

@client.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" " + str(len(bot.guilds)) + " servers | $help"))

async def check_stats_commands(ctx, command, args):
    prefix = await bot.get_prefix(ctx.message)
    if (len(args) != 1 and len(args) != 2):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + command + " {playername} {platform}`. Platform must either be `PC`, `Xbox` or `PS` (or blank for PC).")
            return False
    return True

async def api_down(ctx):
    if (config('APIDOWN') == "true"):
        await ctx.send(":exclamation: The API may be unavailable, please try again later.")


def listen_for_commands():
    while True:
        command = input("Enter command: ")
        if (command.lower() == "save"):
            settings.save_settings()
            print("Settings saved!")




if __name__ == "__main__":
    token = config('HYPERSTATSTEST')
    threading.Thread(target=listen_for_commands).start()
    bot.run(token)
