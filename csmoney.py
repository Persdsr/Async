from aiohttp import ClientSession
import asyncio
import time
import requests


async def csmoney():
    async with ClientSession() as session:
        url = 'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&hasTradeLock=false&hasTradeLock=true&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset=0&tradeLockDays=1&tradeLockDays=2&tradeLockDays=3&tradeLockDays=4&tradeLockDays=5&tradeLockDays=6&tradeLockDays=7&tradeLockDays=0&withStack=true'

        async with session.get(url=url) as response:
            data = await response.json()

            item_json = data.get('items')
            print(item_json)

            for item in item_json:
                print(f'{item["fullName"]}')


async def main():
    task1 = asyncio.create_task(csmoney())

    await task1

print(time.strftime('%X'))

asyncio.run(main())

print(time.strftime('%X'))



