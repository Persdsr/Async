import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import aiohttp
import asyncio

all_items = []

async def get_page_data(session, page):
    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
    }
    url = f'https://www.perekrestok.ru/cat/d?append=1&page=1&page={page}'

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        items = soup.find('div', class_='sc-gTgzIj fTLLNh spinner-container-wrapper').find_all('div', class_='product-card-wrapper')


        for item in items:
            try:
                all_items.append({
                    'title': item.find('div', class_='product-card__title').get_text(strip=True),
                    'new_price': item.find('div', class_=re.compile('price-new')).get_text(strip=True).replace(
                        '\xa0', '').replace('₽', '').replace(',', '.').replace(' ', ''),
                    'old_price': item.find('div', class_=re.compile('price-old-wrapper')).get_text(
                        strip=True).replace('\xa0', '').replace('₽', '').replace(',', '.').replace(' ', ''),
                    # .replace('&nbsp', '')
                    'percent': item.find('div', class_='sc-jcVebW ebkVTf product-card__badge').get_text(
                        strip=True).replace('-', '').replace('%', '').replace(' ', '')
                })
            except:
                continue


async def gather_data():
    ua = UserAgent()
    headers = {
        'user-agent': ua.random,
    }
    url = f'https://www.perekrestok.ru/cat/d?append=1'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        #page_count = int(soup.find("a", class_="sc-fFubgz fNiiPs sc-leCWtA eDsPjK active").get_text()[-1])
        #print(page_count)
        tasks = []

        for page in range(1, 60):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    for item in all_items:
        raz = '{:.2f}'.format(float(item['old_price']) - float(item['new_price']))
        if int(item['percent']) > 1 or 'от' in item['percent']:
            print(f"{item['title']} - {item['new_price']}₽ ({item['old_price']}₽) - {item['percent']}%\n"
                  f"Разница: {raz}₽")
    print(len(all_items))


if __name__ == '__main__':
    main()
