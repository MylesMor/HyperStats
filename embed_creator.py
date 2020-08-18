import discord

async def create_embed(name, stats):
    if name == "best":
        return await create_best_embed(stats)
    elif name == "weapons":
        return await create_weapons_embed(stats)
    elif name == "stats":
        return await create_stats_embed(stats)
    elif name == "hacks":
        return await create_hacks_embed(stats)

async def create_best_embed(stats):
    embed=discord.Embed(title="", color=0x36393f)
    embed.set_author(name=stats['player']['p_name'] + "'s Career Best Statistics", icon_url="https://mylesmor.dev/images/user-icon.png")
    embed.add_field(name="Kills          ", value=stats['data']['stats']['careerbest_kills'], inline=True)
    embed.add_field(name="Assists        ", value=stats['data']['stats']['careerbest_assists'], inline=True)
    embed.add_field(name="Long Range Final Blows        ", value=stats['data']['stats']['careerbest_long_range_final_blows'], inline=True)
    embed.add_field(name="Damage           ", value=stats['data']['stats']['careerbest_damage_done'], inline=True)
    embed.add_field(name="Critical Damage       ‎ ", value=stats['data']['stats']['careerbest_critical_damage'], inline=True)
    embed.add_field(name="Items Fused           ", value=stats['data']['stats']['careerbest_item_fused'], inline=True)
    embed.add_field(name="Items Fused to Max   ‎ ", value=stats['data']['stats']['careerbest_fused_to_max'], inline=True)
    embed.add_field(name="Chests Opened          ‎ ", value=stats['data']['stats']['careerbest_chests'], inline=True)
    embed.add_field(name="Healed        ", value=stats['data']['stats']['careerbest_healed'], inline=True)
    embed.add_field(name="Restores         ", value=stats['data']['stats']['careerbest_revives'], inline=True)
    embed.add_field(name="Survival Time        ‎ ", value=stats['data']['stats']['careerbest_survival_time'], inline=True)
    embed.add_field(name="Damage Shielded           ", value=stats['data']['stats']['careerbest_damage_shielded'], inline=True)
    embed.add_field(name="Enemies Shockwaved         ", value=stats['data']['stats']['careerbest_shockwaved'], inline=True)
    embed.add_field(name="Enemies Revealed          ‎ ", value=stats['data']['stats']['careerbest_revealed'], inline=True)
    embed.add_field(name="Mines Triggered          ‎ ", value=stats['data']['stats']['careerbest_mines_triggered'], inline=True)
    return embed


async def create_hacks_embed(stats):
    mine = stats['data']['hacks']['Mine']
    slam = stats['data']['hacks']['Slam']
    shockwave = stats['data']['hacks']['Shockwave']
    wall = stats['data']['hacks']['Wall']
    heal = stats['data']['hacks']['Heal']
    reveal = stats['data']['hacks']['Reveal']
    teleport = stats['data']['hacks']['Teleport']
    ball = stats['data']['hacks']['Ball']
    invisibility = stats['data']['hacks']['Invisibility']
    invulnerable = stats['data']['hacks']['Armor']
    magnet = stats['data']['hacks']['Magnet']

    embed=discord.Embed(title="", color=0x36393f)
    embed.set_author(name=stats['player']['p_name'] + "'s Hacks Statistics", icon_url="https://mylesmor.dev/images/user-icon.png")
    embed.add_field(name="Mine                           ‎ ", value="_Kills_: " + str(mine['kills']) + "\n_Damage_: " + str(mine['damage']) + "\n_Fusions_: " + str(mine['fusions']), inline=True)
    embed.add_field(name="Slam                           ‎ ", value="_Kills_: " + str(slam['kills']) + "\n_Damage_: " + str(slam['damage']) + "\n_Fusions_: " + str(slam['fusions']), inline=True)
    embed.add_field(name="Shockwave                           ‎ ", value="_Kills_: " + str(shockwave['kills']) + "\n_Damage_: " + str(shockwave['damage']) + "\n_Fusions_: " + str(shockwave['fusions']), inline=True)
    embed.add_field(name="Wall                           ‎ ", value="_Fusions_: " + str(wall['fusions']), inline=True)
    embed.add_field(name="Heal                           ‎ ", value="_Fusions_: " + str(heal['fusions']), inline=True)
    embed.add_field(name="Reveal                           ‎ ", value="_Fusions_: " + str(reveal['fusions']), inline=True)
    embed.add_field(name="Teleport                           ‎ ", value="_Fusions_: " + str(teleport['fusions']), inline=True)
    embed.add_field(name="Ball                           ‎ ", value="_Fusions_: " + str(ball['fusions']), inline=True)
    embed.add_field(name="Invisibility                           ‎ ", value="_Fusions_: " + str(invisibility['fusions']), inline=True)
    embed.add_field(name="Invulnerable                          ‎ ", value="_Fusions_: " + str(invulnerable['fusions']), inline=True)
    embed.add_field(name="Magnet                          ‎ ", value="_Fusions_: " + str(magnet['fusions']), inline=True)
    return embed

async def create_stats_embed(stats):
    embed=discord.Embed(title="", color=0x36393f)
    embed.set_author(name=stats['player']['p_name'] + "'s General Statistics", icon_url="https://mylesmor.dev/images/user-icon.png")
    embed.add_field(name="Wins", value=stats['data']['stats']['wins'], inline=True)
    embed.add_field(name="Crown Wins", value=stats['data']['stats']['crown_wins'], inline=True)
    embed.add_field(name="Winrate", value=stats['data']['stats']['winrate'], inline=True)
    embed.add_field(name="Crown Success", value=stats['data']['stats']['crown_pick_success_rate'], inline=True)
    embed.add_field(name="Kills", value=stats['data']['stats']['kills'], inline=True)
    embed.add_field(name="Assists", value=stats['data']['stats']['assists'], inline=True)
    embed.add_field(name="Avg. Kills per Match     ", value=stats['data']['stats']['avg_kills_per_match'], inline=True)
    embed.add_field(name="K/D", value=stats['data']['stats']['kd'], inline=True)
    embed.add_field(name="Damage Done", value=stats['data']['stats']['damage_done'], inline=True)
    embed.add_field(name="Avg. Damage per Kill        ‎", value=stats['data']['stats']['avg_dmg_per_kill'], inline=True)
    embed.add_field(name="Headshot Accuracy         ‎", value=stats['data']['stats']['headshot_accuracy'], inline=True)
    embed.add_field(name="Restores", value=stats['data']['stats']['revives'], inline=True)
    embed.add_field(name="Fusions", value=stats['data']['stats']['fusions'], inline=True)
    embed.add_field(name="Chests Broken", value=stats['data']['stats']['chests_broken'], inline=True)
    embed.add_field(name="Time Played", value=stats['data']['stats']['time_played'], inline=True)

    """
    embed=discord.Embed(color=0x66bdff)
    embed.set_author(name=stats['player']['p_name'] + "'s Statistics")
    embed.add_field(name="Wins", value="Wins: " + str(stats['data']['stats']['wins']) + "\nCrown Wins: " + str(stats['data']['stats']['crown_wins']) + "\nWinrate: " + str(stats['data']['stats']['winrate']) + "\nCrown Success: " + str(stats['data']['stats']['crown_pick_success_rate']) , inline=True)
    embed.add_field(name="Kills", value="Kills: " + str(stats['data']['stats']['kills']) + "\nAssists: " + str(stats['data']['stats']['assists']) + "\nAvg. Kills per Match: " + str(stats['data']['stats']['avg_kills_per_match']) + "\nK/D: " + str(stats['data']['stats']['kd']) , inline=True)
    embed.add_field(name="Damage", value="Damage Done: " + str(stats['data']['stats']['damage_done']) + "\nAvg. Damager per Kill: " + str(stats['data']['stats']['avg_dmg_per_kill']) + "\nHeadshot Accuracy: " + str(stats['data']['stats']['headshot_accuracy']), inline=True)
    embed.add_field(name="Restores", value=stats['data']['stats']['revives'], inline=True)
    embed.add_field(name="Fusions", value=stats['data']['stats']['fusions'], inline=True)
    embed.add_field(name="Chests Broken", value=stats['data']['stats']['chests_broken'], inline=True)
    embed.add_field(name="Time Played", value=stats['data']['stats']['time_played'], inline=True)
    """
    return embed

async def create_weapons_embed(stats):
    dragonfly = stats['data']['weapons']['Dragon Fly']
    mammoth = stats['data']['weapons']['Mammoth MK1']
    ripper = stats['data']['weapons']['The Ripper']
    dtap = stats['data']['weapons']['D-Tap']
    harpy = stats['data']['weapons']['Harpy']
    komodo = stats['data']['weapons']['Komodo']
    hexfire = stats['data']['weapons']['Hexfire']
    riotone = stats['data']['weapons']['Riot One']
    salvo = stats['data']['weapons']['Salvo EPL']
    skybreaker = stats['data']['weapons']['Skybreaker']
    protocol = stats['data']['weapons']['Protocol V']

    embed=discord.Embed(title="", color=0x36393f)
    embed.set_author(name=stats['player']['p_name'] + "'s Weapons Statistics", icon_url="https://mylesmor.dev/images/user-icon.png")
    embed.add_field(name="Dragonfly                           ‎ ", value="_Kills_: " + str(dragonfly['kills']) + "\n_Damage_: " + str(dragonfly['damage']) + "\n_Headshot Damage_: " + str(dragonfly['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(dragonfly['hs_accuracy']) + "%" + "\n_Fusions_: " + str(dragonfly['fusions']), inline=True)
    embed.add_field(name="Mammoth MK1                         ‎ ", value="_Kills_: " + str(mammoth['kills']) + "\n_Damage_: " + str(mammoth['damage']) + "\n_Headshot Damage_: " + str(mammoth['headshot_damage'])  + "             ‎\n_Headshot Accuracy_: " + str(mammoth['hs_accuracy']) + "%" + "\n_Fusions_: " + str(mammoth['fusions']), inline=True)
    embed.add_field(name="Ripper                              ‎ ", value="_Kills_: " + str(ripper['kills']) + "\n_Damage_: " + str(ripper['damage']) + "\n_Headshot Damage_:" + str(ripper['headshot_damage'])  + "‎‎‎             ‎‎‎‎\n_Headshot Accuracy_: " + str(ripper['hs_accuracy']) + "%" + "\n_Fusions_: " + str(ripper['fusions']), inline=True)
    embed.add_field(name="D-Tap                               ‎ ", value="_Kills_: " + str(dtap['kills']) + "\n_Damage_: " + str(dtap['damage']) + "\n_Headshot Damage_: " + str(dtap['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(dtap['hs_accuracy']) + "%" + "\n_Fusions_: " + str(dtap['fusions']), inline=True)
    embed.add_field(name="Harpy                               ‎ ", value="_Kills_: " + str(harpy['kills']) + "\n_Damage_: " + str(harpy['damage']) + "\n_Headshot Damage_: " + str(harpy['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(harpy['hs_accuracy']) + "%" + "\n_Fusions_: " + str(harpy['fusions']), inline=True)
    embed.add_field(name="Komodo                              ‎ ", value="_Kills_: " + str(komodo['kills']) + "\n_Damage_: " + str(komodo['damage']) + "\n_Headshot Damage_: " + str(komodo['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(komodo['hs_accuracy']) + "%" + "\n_Fusions_: " + str(komodo['fusions']), inline=True)
    embed.add_field(name="Hexfire                             ‎ ", value="_Kills_: " + str(hexfire['kills']) + "\n_Damage_: " + str(hexfire['damage']) + "\n_Headshot Damage_: " + str(hexfire['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(hexfire['hs_accuracy']) + "%" + "\n_Fusions_: " + str(hexfire['fusions']), inline=True)
    embed.add_field(name="Riot One                           ‎  ", value="_Kills_: " + str(riotone['kills']) + "\n_Damage_: " + str(riotone['damage']) + "\n_Headshot Damage_: " + str(riotone['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(riotone['hs_accuracy']) + "%" + "\n_Fusions_: " + str(riotone['fusions']), inline=True)
    embed.add_field(name="Salvo EPL                           ‎ ", value="_Kills_: " + str(salvo['kills']) + "\n_Damage_: " + str(salvo['damage']) + "\n_Headshot Damage_: " + str(salvo['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(salvo['hs_accuracy']) + "%" + "\n_Fusions_: " + str(salvo['fusions']), inline=True)
    embed.add_field(name="Skybreaker                          ‎ ", value="_Kills_: " + str(skybreaker['kills']) + "\n_Damage_: " + str(skybreaker['damage']) + "\n_Headshot Damage_: " + str(skybreaker['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(skybreaker['hs_accuracy']) + "%" + "\n_Fusions_: " + str(skybreaker['fusions']), inline=True)
    embed.add_field(name="Protocol V                          ‎ ", value="_Kills_: " + str(protocol['kills']) + "\n_Damage_: " + str(protocol['damage']) + "\n_Headshot Damage_: " + str(protocol['headshot_damage'])  + "\n_Headshot Accuracy_: " + str(protocol['hs_accuracy']) + "%" + "\n_Fusions_: " + str(protocol['fusions']), inline=True)
    return embed

async def create_about_embed():
    embed=discord.Embed(title=" ", url="https://github.com/MylesMor/HyperStats", description="An unofficial Discord bot for Hyper Scape statistics!", color=0x36393f)
    embed.set_author(name="HyperStats by MylesMor", url="https://github.com/MylesMor/HyperStats", icon_url="https://mylesmor.dev/images/user-icon.png")
    embed.set_thumbnail(url="https://mylesmor.dev/resources/sunglasses.PNG")
    embed.add_field(name="Help", value="[GitHub](https://github.com/MylesMor/HyperStats)", inline=True)
    embed.set_footer(text="Version 1.0.0")
    return embed
