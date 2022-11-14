import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_televisions():
    ua = UserAgent()
    page = 1
    url = f'https://www.mvideo.ru/product-list-page?q=телефон&category=smartfony-205'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.5.716 Yowser/2.5 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, 'lxml')
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print(soup)
    print(soup.find('a'))
    items = soup.find('div', class_='plp__card-grid').find_all('div', class_='product-cards-layout__item ng-star-inserted')
    all_items = []

    for item in items:
        all_items.append({
            'title': item.find('a', class_='product-title__text').get_text(),
            'price': item.find('span', class_='price__main-value').replace('&nbsp;', ' ')
        })
    return all_items


def main():
    products = get_televisions()
    for item in products:
        print(f"{item['title']} - {item['price']}")
        print('---------------------------------------')


if __name__ == '__main__':
    main()
