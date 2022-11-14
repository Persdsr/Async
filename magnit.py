import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_promo():
    ua = UserAgent()
    url = 'https://magnit.ru/promo/?format[]=mm'
    headers = {
        'user-agent': ua.random}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    items = soup.find('div', class_='сatalogue__main js-promo-container').find_all('a', class_='card-sale card-sale_catalogue')
    all_promo = []

    for item in items:
        all_promo.append(
            {
                'title': item.find('div', class_='card-sale__title').find('p').get_text(),
                'old_price': int(item.find('span', class_='label__price-integer').get_text()),
                'new_price': int(item.find('div', class_='label__price label__price_new').find('span', class_='label__price-integer').get_text())
            }
        )
    return all_promo


def main():
    products = get_promo()

    for product in products:
        print(f'{product["title"]}\nСтарая цена - {product["old_price"]}\nНовая цена - {product["new_price"]}\nРазница - {product["old_price"]-product["new_price"]}')
        print('--------------------------------')
    print(len(products))
#записать в csv файл продукты с ценой продоктов с акцией снизился на n%
if __name__ == '__main__':
    main()