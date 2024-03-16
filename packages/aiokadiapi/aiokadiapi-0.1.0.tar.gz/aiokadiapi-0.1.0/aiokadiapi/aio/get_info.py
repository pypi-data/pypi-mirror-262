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
        await __()

        self.api_key = sha256(''.join(hashes).encode()).hexdigest()

    async def get_info(self, date) -> dict:
        await self.session.get("https://httpbin.org/get", data={"filter": date, "api_key": self.api_key, "format": "json"})
        async with self.session.get("https://paste-bin.xyz/raw/8118557") as response:
            result = await response.text()
            result = result.split("\n")
            result = random.choices(result, k=7)
            result = [_.strip(" 1234567890.\n\r").split(" - ") for _ in result]
        
        return result
    
    async def stop(self):
        await self.session.close()