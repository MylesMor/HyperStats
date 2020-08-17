import time

class Cache():
    def __init__(self):
        self.cache = {"uplay": {}, "psn": {}, "xbl": {}}
        self.cache_time = 300

    async def add_player_to_cache(self, stats):
        if stats['player']['p_name'] not in self.cache[stats['player']['p_platform']]:
            await self.update_cache(stats)

    async def update_cache(self, stats):
        self.cache[stats['player']['p_platform']][stats['player']['p_name'].lower()] = {"last_update": time.time(), "stats": stats}
        return True
        

    async def check_cache(self, playername, platform):
        if playername.lower() in self.cache[platform]:
            last_update = self.cache[platform][playername.lower()]['last_update']
            if time.time() - last_update <= self.cache_time:
                return self.cache[platform][playername.lower()]['stats']
        return None 

    async def get_update_string(self, playername, platform):
        return " Cached copy - updating in " + str(int(self.cache_time - (time.time() - self.cache[platform][playername]['last_update']))) + " seconds." 
