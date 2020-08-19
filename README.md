# HyperStats
An unofficial Discord bot for Hyper Scape statistics!

# Usage
Invite to server using this link: https://discord.com/api/oauth2/authorize?client_id=744530482410291341&permissions=522304&scope=bot

The default prefix is `$`.

To see all commands, type `$help` or look at the Commands section below.

## Commands

### Admin commands
`$setprefix {prefix}`: Changes the bot prefix (admin only).

`$disablechannel`: Disables the bot in the channel this command is used in for non-administrators (admin only).

`$enablechannel`: Enables the bot in the channel this command is used in for non-administrators (admin only).

`$listdisabledchannels`: Lists all disabled channels. (admin only).

### General Commands
`$help`: Displays this menu.

`$about`: Displays information about this bot.

`$link {playername} {platform}`: Links your discord account to your in-game account. Once complete, you can use the below commands without any arguments to view your own stats.

`$unlink`: Unlinks your in-game account from your discord account.


For all of the below commands, platform must be either be empty for PC, or one of PC, Xbox or PS. You can also use `$link {playername} {platform}` to use the below commands to view your own stats without any arguments.


`$stats {playername} {platform}`: Displays player stats.

`$weapons {playername} {platform}`: Displays weapon stats for a player.

`$hacks {playername} {platform}`: Displays hack stats for a player.

`$best {playername} {platform}`: Displays career best stats for a player (best in one game).


All of the above four stats commands are cached for 5 minutes, and will automatically update after this time. Therefore you won't see any changes that occur until the next update (this time is listed above the statistics embed).

## Example output

`$stats` example output:

![Stats](https://github.com/MylesMor/HyperStats/blob/master/images/stats.png?raw=true)

`$weapons` example output:

![Stats](https://github.com/MylesMor/HyperStats/blob/master/images/weapons.png?raw=true)

`$hacks` example output:

![Stats](https://github.com/MylesMor/HyperStats/blob/master/images/hacks.png?raw=true)

`$best` example output:

![Stats](https://github.com/MylesMor/HyperStats/blob/master/images/best.png?raw=true)
