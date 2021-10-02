import aiohttp
import json

async def get_requests_as_json(url, headers=None):
	async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                r = await resp.json(content_type=None)
                return r

async def get_requests_as_text(url, headers=None):
	async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                r = await resp.text()
                return r