import discord
from discord.ext import commands
from settings import Settings
import embed_creator
import requests
import json
import os
from decouple import config

settings = None

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
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send("<><><><><><><> :grey_question: HyperStats Help :grey_question: <><><><><><><>\n\n Prefix: `" + prefix + "`\n\n`" + prefix + "setprefix {prefix}`: Changes the bot prefix **(admin only)**.\n`" + prefix + "disablechannel`: Disables the bot in the channel this command is used in for non-administrators **(admin only)**.\n`" + prefix + "enablechannel`: Enables the bot in the channel this command is used in for non-administrators **(admin only)**.\n\n`" + prefix + "help`: Displays this menu.\n`" + prefix + "stats {playername} {platform}`: Displays player stats. Platform must be PC, Xbox, or PS.\n`" + prefix + "weapons {playername} {platform}`: Displays weapon stats for a player. Platform must be PC, Xbox, or PS.\n`" + prefix + "hacks {playername} {platform}`: Displays hack stats for a player. Platform must be PC, Xbox, or PS.\n`" + prefix + "best {playername} {platform}`: Displays career best stats for a player (best in one game). Platform must be PC, Xbox, or PS.")
    else:
        await ctx.send("<><><><><><><> :grey_question: HyperStats Help :grey_question: <><><><><><><>\n\n Prefix: " + prefix + "\n\n`" + prefix + "help`: Displays this menu.\n`" + prefix + "stats {playername} {platform}`: Displays player stats. Platform must be PC, Xbox, or PS.\n`" + prefix + "weapons {playername} {platform}`: Displays weapon stats for a player. Platform must be PC, Xbox, or PS.\n`" + prefix + "hacks {playername} {platform}`: Displays hack stats for a player. Platform must be PC, Xbox, or PS.\n`" + prefix + "best {playername} {platform}`: Displays career best stats for a player (best in one game). Platform must be PC, Xbox, or PS.")


@bot.command()
@commands.check(is_disabled)
async def stats(ctx, *args):
    if (len(args) != 2):
        prefix = await bot.get_prefix(ctx.message)
        await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "stats {playername} {platform}`. Platform must be either PC, Xbox or PS.")
        return False
    else:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        id = await find_player(status, args[0], args[1])
        if id:
            stats = await get_player_stats(status, id["p_name"], id["p_id"])
            if stats:
                embed = await embed_creator.create_stats_embed(stats)
                await status.edit(content="", embed=embed)



@bot.command()
@commands.check(is_disabled)
async def weapons(ctx, *args):
    if (len(args) != 2):
        prefix = await bot.get_prefix(ctx.message)
        await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "weapons {playername} {platform}`. Platform must be either PC, Xbox or PS.")
        return False
    else:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        id = await find_player(status, args[0], args[1])
        if id:
            stats = await get_player_stats(status, id["p_name"], id["p_id"])
            if stats:
                embed = await embed_creator.create_weapons_embed(stats)
                await status.edit(content="", embed=embed)


@bot.command()
@commands.check(is_disabled)
async def best(ctx, *args):
    if (len(args) != 2):
        prefix = await bot.get_prefix(ctx.message)
        await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "best {playername} {platform}`. Platform must be either PC, Xbox or PS.")
        return False
    else:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        id = await find_player(status, args[0], args[1])
        if id:
            stats = await get_player_stats(status, id["p_name"], id["p_id"])
            if stats:
                embed = await embed_creator.create_best_embed(stats)
                await status.edit(content="", embed=embed)


@bot.command()
@commands.check(is_disabled)
async def hacks(ctx, *args):
    if (len(args) != 2):
        prefix = await bot.get_prefix(ctx.message)
        await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "hacks {playername} {platform}`. Platform must be either PC, Xbox or PS.")
        return False
    else:
        status = await ctx.send(":hourglass: Finding player " + args[0] + "...")
        id = await find_player(status, args[0], args[1])
        if id:
            stats = await get_player_stats(status, id["p_name"], id["p_id"])
            if stats:
                embed = await embed_creator.create_hacks_embed(stats)
                await status.edit(content="", embed=embed)


@bot.command()
async def disablechannel(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 0):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "disablechannel`. Use this command in the channel you'd like to disable the bot in!")
        else:
            disable = await settings.disable_channel(ctx.message.guild.id, ctx.message.channel.id)
            if disable:
                ctx.send(":white_check_mark: Bot **disabled** in channel for non-administrators.")

@bot.command()
async def enablechannel(ctx, *args):
    prefix = await bot.get_prefix(ctx.message)
    if ctx.message.author.guild_permissions.administrator:
        if (len(args) != 0):
            await ctx.send("**:stop_sign: Invalid command!** Correct usage: `" + prefix + "enablechannel`. Use this command in the channel you'd like to enable the bot in!")
        else:
            enable = await settings.enable_channel(ctx.message.guild.id, ctx.message.channel.id)
            if enable:
                ctx.send(":white_check_mark: Bot **enabled** in channel for non-administrators.")

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
    print(platform.lower() == "pc")
    if platform.lower() != "pc" and platform.lower() != "xbox" and platform.lower() != "ps":
        await status.edit(content=":exclamation: **Invalid platform!** Platform must be `PC`, `Xbox` or `PS`.")
        return False
    if platform.lower() == "pc":
        platform = "uplay"
    elif platform.lower() == "xbox":
        platform = "xbl"
    elif platform.lower() == "ps":
        platform = "psn"
    r = requests.get("https://hypers.apitab.com/search/" + platform + "/" + playername)
    if r.status_code == 200:
        print(r.json())
        players = r.json()['players']
        for _, player in players.items():
            if player['profile']['p_name'].lower() == playername.lower():
                return player['profile']
    await status.edit(content=":exclamation: Failed to find " + playername + " on platform " + platform + "!")
    return False


async def get_player_stats(status, playername, player_id):
    await status.edit(content=":hourglass: Retrieving stats for player " + playername + "...")
    r = requests.get("https://hypers.apitab.com/update/" + player_id)
    if r.status_code == 200:
        return r.json()
    else:
        return False



if __name__ == "__main__":
    token = config('HYPERSTATS')
    bot.run(token)
