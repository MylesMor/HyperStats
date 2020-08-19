import threading
import json
import os

class Settings():
    def __init__(self):
        self.check_for_file()
        self.settings = self.get_settings()
        self.links = self.get_links()
        self.time_between_saves = 300
        self.save_settings()
    
    def check_for_file(self):
        if not os.path.isfile("guilds.json"):
            with open("guilds.json", 'w+') as f:
                f.write("{}")
        if not os.path.isfile("links.json"):
            with open("links.json", 'w+') as f:
                    f.write("{}")


    def get_settings(self):
        with open("guilds.json", 'r') as f:
            return json.load(f)

    def get_links(self):
            with open("links.json", 'r') as f:
                return json.load(f)
        
    async def add_link(self, user_id, player_id, playername, platform):
        self.links[str(user_id)] = {"p_name": playername, "p_id": player_id, "p_platform": platform}

    async def remove_link(self, user_id):
        self.links.pop(str(user_id))

    async def get_linked_user(self, user_id):
        if str(user_id) in self.links:
            return self.links[str(user_id)]
        return None



    async def set_prefix(self, guild_id, prefix):
        await self.add_guild_to_settings(guild_id)
        self.settings[str(guild_id)]['prefix'] = prefix
        return True
    

    async def add_guild_to_settings(self, guild_id):
        if str(guild_id) not in self.settings:
            self.settings[str(guild_id)] = {'prefix': '$', 'disabledchannels': []}


    async def get_prefix(self, guild_id):
        await self.add_guild_to_settings(guild_id)
        return self.settings[str(guild_id)]['prefix']


    async def disable_channel(self, guild_id, channel_id):
        await self.add_guild_to_settings(guild_id)
        self.settings[str(guild_id)]['disabledchannels'].append(channel_id)
        return True
    
    async def enable_channel(self, guild_id, channel_id):
        await self.add_guild_to_settings(guild_id)
        if channel_id not in self.settings[str(guild_id)]['disabledchannels']:
            return False
        self.settings[str(guild_id)]['disabledchannels'].remove(channel_id)
        return True

    async def check_disabled_channel(self, guild_id, channel_id):
        await self.add_guild_to_settings(guild_id)
        if channel_id in self.settings[str(guild_id)]['disabledchannels']:
            return True
        return False

    async def get_disabled_channels(self, guild_id):
        await self.add_guild_to_settings(guild_id)
        channel_string = "**Disabled channels:** "
        for channel in self.settings[str(guild_id)]['disabledchannels']:
            channel_string += "<#" + str(channel) + ">, "
        return channel_string[:-2]

    def save_settings(self):
        threading.Timer(self.time_between_saves, self.save_settings).start()
        with open("guilds.json", 'w') as f:
            json.dump(self.settings, f)
        with open("links.json", 'w') as f:
            json.dump(self.links, f)
            



