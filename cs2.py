import json

import asyncio
import aiohttp
import time

start_time = time.time()
all_date = []


async def collect_data():
    offset = 0
    batch_size = 60
    result = []
    count = 0
    items = []
    for item in range(offset, offset + batch_size, 60):
        async with aiohttp.ClientSession() as session:
            url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&hasTradeLock=false&hasTradeLock=true&isStore=true&limit=60&maxPrice=120&minPrice=1&offset=60&tradeLockDays=1&tradeLockDays=2&tradeLockDays=3&tradeLockDays=4&tradeLockDays=5&tradeLockDays=6&tradeLockDays=7&tradeLockDays=0&withStack=true'

            async with session.get(url) as resp:

                data = await resp.json()
                items = data.get('items')

                offset += batch_size

                for i in items:
                    if i.get('overprice') is not None and i.get('overprice') < 10:
                        item_full_name = i.get('fullName')
                        item_3d = i.get('3d')
                        item_price = i.get('price')
                        item_over_price = i.get('overprice')
                        result.append(
                            {
                                'full_name': item_full_name,
                                '3d': item_3d,
                                'overprice': item_over_price,
                                'item_price': item_price
                            }
                        )
                        print(f'{i}')
                print('------------------------------------------------')
                print('------------------------------------------------')
                print('------------------------------------------------')
                print('------------------------------------------------')
                count += 1
                print(count)

async def main():
    tasks = []
    for offset_id in range(3):
        task = asyncio.create_task(collect_data())
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())

end_time = time.time() - start_time
print(all_date)


