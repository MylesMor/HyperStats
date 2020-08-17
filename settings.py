import threading
import json
import os

class Settings():
    def __init__(self):
        self.check_for_file()
        self.settings = self.get_settings()
        self.save_settings()

    
    def check_for_file(self):
        if not os.path.isfile("guilds.json"):
            with open("guilds.json", 'w+') as f:
                f.write("{}")


    def get_settings(self):
        with open("guilds.json", 'r') as f:
            return json.load(f)
        


    async def set_prefix(self, guild_id, prefix):
        await self.add_guild_to_settings(guild_id)
        print(self.settings)
        self.settings[str(guild_id)]['prefix'] = prefix
        print(self.settings)
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
        threading.Timer(2, self.save_settings).start()
        with open("guilds.json", 'w') as f:
            json.dump(self.settings, f)


