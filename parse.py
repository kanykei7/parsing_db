import requests
from bs4 import BeautifulSoup
from db import Request


class Parser:
    def __init__(self, url, host: str):
        self.url = url
        self.HEADERS = {
            'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'
        }
        self.HOST = host

    def get_html(self, params=''):
        r = requests.get(url=self.url, headers=self.HEADERS, params=params)
        return r

    def get_content(self, html):
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='item product_listbox oh')
        new_list = []
        for item in items:
            new_list.append({
                'title': item.find('div', class_='listbox_title oh').find('a').get_text(strip=True),
                'price': item.find('div', class_='listbox_price text-center').get_text(strip=True),
                'images': self.HOST + item.find('div', class_='listbox_img pull-left').find('img').get('src')
            })
        return new_list

    def save(self, items):
        db = Request('kivano', 'title', 'price', 'images')
        for item in items:
            db.write_values(item['title'], item['price'], item['images'])
        print('Insert success')

    def parse(self, page: int):
        for pg in range(1, page+1):
            html = self.get_html(params={'page': pg})
            if html.status_code == 200:
                self.save(self.get_content(html))
                print(f'page {pg} insert success')
            else:
                print("Не удалось достучаться до сайта!")


parse = Parser("https://www.kivano.kg/noutbuki", "https://www.kivano.kg")
parse.parse(2)
