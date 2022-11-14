
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import aiohttp
import asyncio

async def get_discount():
    ua = UserAgent()
    page = 1
    headers = {
        'user-agent': ua.random,
    }
    all_items = []
    try:
        url = f'https://www.perekrestok.ru/cat/d?append=1&page={page}'
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=headers)
            soup = BeautifulSoup(await response.text(), 'lxml')
            items = soup.find('div', class_='sc-gTgzIj fTLLNh spinner-container-wrapper').find_all('div', class_='product-card-wrapper')
            for item in items:
                try:
                    all_items.append({
                        'title': item.find('div', class_='product-card__title').get_text(strip=True),
                        'new_price': item.find('div', class_=re.compile('price-new')).get_text(strip=True).replace('\xa0', '').replace('₽', '').replace(',', '.').replace(' ', ''),
                        'old_price': item.find('div', class_=re.compile('price-old-wrapper')).get_text(strip=True).replace('\xa0', '').replace('₽', '').replace(',', '.').replace(' ', ''),#.replace('&nbsp', '')
                        'percent': item.find('div', class_='sc-jcVebW ebkVTf product-card__badge').get_text(strip=True).replace('-', '').replace('%', '').replace(' ', '')
                    })
                except:
                    continue
            page += 1
    except:
        return all_items


async def main():
    products = await get_discount()

    for item in products:
        raz = '{:.2f}'.format(float(item['old_price']) - float(item['new_price']))
        if int(item['percent']) > 1:
            print(f"{item['title']} - {item['new_price']}₽ ({item['old_price']}₽) - {item['percent']}%\n"
                  f"Разница: {raz}₽")
    print(len(products))


if __name__ == '__main__':
    asyncio.run(main())
