import aiohttp
from cache import Cache
import embed_creator

cache = Cache()

async def find_player(status, playername, platform):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://hypers.apitab.com/search/" + platform + "/" + playername) as resp:
            status_code = resp.status
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

async def manage_stats_commands(ctx, status, playername, platform, id=None):
    if id is None:
        found_id = await find_player(status, playername, platform)
        if found_id:
            stats = await get_player_stats(status, found_id["p_name"], found_id["p_id"])
            return stats
    else:
        stats = await get_player_stats(status, playername, id)


async def show_statistics(ctx, status, command, playername, platform, id_found=False):
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

async def check_for_linked_user(settings, ctx, args, command):
    user = await settings.get_linked_user(ctx.message.author.id)
    if user is not None:
        status = await ctx.send(":hourglass: Finding player " + user['p_name'] + "...")
        await show_statistics(ctx, status, command, user['p_name'], user['p_platform'], id_found=user['p_id'])
        return True
    return False

async def is_linked(settings, ctx, args, command):
    if (len(args) == 0):
        linked = await check_for_linked_user(settings, ctx, args, command)
        if linked:
            return True
    return False
