import discord
from discord.ext import commands
from settings import Settings
from cache import Cache
import embed_creator
import json
import os
from decouple import config
import time
import aiohttp


def determine_prefixes(bot, message):
    return settings.get_prefix(message.guild.id)

cache = Cache()
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
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send("<><><><><><><> :grey_question: HyperStats Help :grey_question: <><><><><><><>\n\n Prefix: `" + prefix + "`\n\n`" + prefix + "setprefix {prefix}`: Changes the bot prefix **(admin only)**.\n`" + prefix + "disablechannel`: Disables the bot in the channel this command is used in for non-administrators **(admin only)**.\n`" + prefix + "enablechannel`: Enables the bot in the channel this command is used in for non-administrators **(admin only)**.\n\n`" + prefix + "help`: Displays this menu.\n`" + prefix + "about`: Displays information about this bot.\n\nFor all of the below commands, platform must be either be empty for PC, or one of `PC`, `Xbox` or `PS`.\n\n`" + prefix + "stats {playername} {platform}`: Displays player stats.\n`" + prefix + "weapons {playername} {platform}`: Displays weapon stats for a player.\n`" + prefix + "hacks {playername} {platform}`: Displays hack stats for a player.\n`" + prefix + "best {playername} {platform}`: Displays career best stats for a player (best in one game).")
    else:
        await ctx.send("<><><><><><><> :grey_question: HyperStats Help :grey_question: <><><><><><><>\n\n Prefix: " + prefix + "\n\n`" + prefix + "help`: Displays this menu.\n`" + prefix + "about`: Displays information about this bot.\n\nFor all of the below commands, platform must be either be empty for PC, or one of `PC`, `Xbox` or `PS`.\n\n`" + prefix + "stats {playername} {platform}`: Displays player stats.\n`" + prefix + "weapons {playername} {platform}`: Displays weapon stats for a player.\n`" + prefix + "hacks {playername} {platform}`: Displays hack stats for a player.\n`" + prefix + "best {playername} {platform}`: Displays career best stats for a player (best in one game).")


@bot.command()
@commands.check(is_disabled)
async def stats(ctx, *args):
    if (config('APIDOWN') == "true"):
        await ctx.send(":exclamation: The API may be unavailable, please try again later.")
    valid = await check_stats_commands(ctx, "stats", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await determine_platform(status, args)
        await show_statistics(ctx, status, "stats", args[0], platform)



@bot.command()
@commands.check(is_disabled)
async def weapons(ctx, *args):
    if (config('APIDOWN') == "true"):
        await ctx.send(":exclamation: The API may be unavailable, please try again later.")
    valid = await check_stats_commands(ctx, "weapons", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await determine_platform(status, args)
        await show_statistics(ctx, status, "weapons", args[0], platform)


@bot.command()
@commands.check(is_disabled)
async def best(ctx, *args):
    if (config('APIDOWN') == "true"):
        await ctx.send(":exclamation: The API may be unavailable, please try again later.")
    valid = await check_stats_commands(ctx, "best", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await determine_platform(status, args)
        await show_statistics(ctx, status, "best", args[0], platform)

@bot.command()
@commands.check(is_disabled)
async def hacks(ctx, *args):
    if (config('APIDOWN') == "true"):
        await ctx.send(":exclamation: The API may be unavailable, please try again later.")
    valid = await check_stats_commands(ctx, "hacks", args)
    if valid:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        platform = await determine_platform(status, args)
        await show_statistics(ctx, status, "hacks", args[0], platform)

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

#################### HELPER ####################

async def find_player(status, playername, platform):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://hypers.apitab.com/search/" + platform + "/" + playername) as resp:
            status_code = resp.status
            print(status_code)
            if status_code == 200:
                data = await resp.json()
                if "players" in data:
                    players = data['players']
                    if len(players) != 0:
                        for _, player in players.items():
                            if player['profile']['p_name'].lower() == playername.lower():
                                return player['profile']
            else:
                await status.edit(content=":exclamation: Failed to find player **" + playername + "**! The API is unavailable, please try again later.")
                return False
    await status.edit(content=":exclamation: Failed to find player **" + playername + "**!")
    return False


async def get_player_stats(status, playername, player_id):
    await status.edit(content=":hourglass: Retrieving stats for player " + playername + "...")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://hypers.apitab.com/update/" + player_id) as resp:
            status_code = resp.status
            if status_code == 200:
                json_data = await resp.json()
                if "found" in json_data:
                    if json_data['found']:
                        return json_data
            else:
                await status.edit(content=":exclamation: Failed to find player **" + playername + "**! The API is unavailable, please try again later.")
                return False
    await status.edit(content=":exclamation: Failed to retrieve stats for **" + playername + "**!")
    return False


async def determine_platform(status, args):
    if len(args) == 1:
        return "uplay"
    elif len(args) == 2:
        platform = args[1]
        if platform.lower() != "pc" and platform.lower() != "xbox" and platform.lower() != "ps":
            await status.edit(content=":exclamation: **Invalid platform!** Platform must be `PC`, `Xbox` or `PS`.")
            return False
        if platform.lower() == "pc":
            platform = "uplay"
        elif platform.lower() == "xbox":
            platform = "xbl"
        elif platform.lower() == "ps":
            platform = "psn"
        return platform

async def manage_stats_commands(ctx, status, playername, platform):
    id = await find_player(status, playername, platform)
    if id:
        stats = await get_player_stats(status, id["p_name"], id["p_id"])
        return stats


async def check_stats_commands(ctx, command, args):
    prefix = await bot.get_prefix(ctx.message)
    if (len(args) != 1 and len(args) != 2):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + command + " {playername} {platform}`. Platform must either be `PC`, `Xbox` or `PS` (or blank for PC).")
            return False
    return True

async def show_statistics(ctx, status, command, playername, platform):
    cached = await cache.check_cache(playername, platform)
    if cached is None:
        stats = await manage_stats_commands(ctx, status,playername, platform)
        if stats is not None:
            await cache.add_player_to_cache(stats)
            await cache.update_cache(stats)
        else:
            print("Retreiving stats failed. Is the API down?")
    else:
        stats = cached
    if stats:
        embed = await embed_creator.create_embed(command, stats)
        if cached is not None:
            cached_string = await cache.get_update_string(playername.lower(), platform)
            await status.edit(content=cached_string, embed=embed)
            return
        else:
            await cache.update_cache(stats)
        await status.edit(content="", embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" " + str(len(bot.guilds)) + " servers | $help"))

@client.event
async def on_guild_join(guild):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" " + str(len(bot.guilds)) + " servers | $help"))


if __name__ == "__main__":
    token = config('HYPERSTATS')
    bot.run(token)
