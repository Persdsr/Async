import requests
from bs4 import BeautifulSoup
import datetime
from fake_useragent import UserAgent


def collect_data(city_code):
    cur_time = datetime.datetime.now().strftime('%d_%M_%Y_%H_%M')
    ua = UserAgent().random
    cookies = {
        'mg_geo_id': city_code
    }
    headers = {
        'Accept': '*/*',
        'User-Agent': ua.random,
        'X-Requested-With': 'XMLHttpRequest'
    }

    resp = requests.get(url='https://magnit.ru/promo/?format[]=mm', headers=headers).text
    soup = BeautifulSoup(resp, 'lxml')
    city = soup.find('a', class_='header__contacts-link_city').text.strip()

    list_data = []

    page = 1
    while resp:
        data = {
            'page': f'{page}'
        }

        resp = requests.get('https://magnit.ru/promo/?format[]=mm', cookies=cookies, headers=headers, data=data).text
        print(resp)
        soup = BeautifulSoup(resp, 'lxml')

        list_cards = soup.find_all('a', class_='card-sale_catalogue')

        for card in list_cards:

            try:
                card_discount = card.find('div', class_='card-sale__discount').text.strip()
            except AttributeError:
                continue

            card_title = card.find('div', class_='card-sale__title').text.strip()


def main():
    collect_data(city_code='1626')


if __name__ == '__main__':
    main()
