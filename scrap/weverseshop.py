import requests
from bs4 import BeautifulSoup


async def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', {'class': 'sc-ee91b503-2 kDyufS'})

    result = []
    for item in items:
        title = item.find('a')['title']
        img_tags = item.find_all('img')
        if len(img_tags) >= 2:
            img_src = img_tags[1]['src']
        else:
            img_src = img_tags[0]['src']
        item_url = "https://shop.weverse.io" + item.find('a')['href']

        price = item.find('figcaption', {'class': 'sc-fb17985a-5 dIWEfZ'}).find('strong',
                                                                                {'class': 'sc-d4956143-2 JDTLz'}).text

        is_sold_out = item.find('figcaption', {'class': 'sc-fb17985a-5 dIWEfZ'}).find('strong', {
            'class': 'sc-fb17985a-1 ipzbQw'}) is not None

        result.append({'title': title, 'img_src': img_src, 'url': item_url, 'price': price, 'is_sold_out': is_sold_out})

    return result


async def get_items():
    page = 1
    items = []

    while True:
        url = f"https://shop.weverse.io/ko/shop/GL_KRW/artists/35/categories/615?page={page}"
        page_items = await parse_page(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        no_items = soup.find('div', {'class': 'sc-eef0fdb-5 iSLDTU'})

        if no_items and "등록된 상품이 없습니다" in no_items.text:
            break

        items.extend(page_items)
        page += 1

    return items
