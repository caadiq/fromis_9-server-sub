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

        item_url = item.find('a')['href']
        url = "https://shop.weverse.io" + item_url
        item_id = item_url.split('/')[-1]

        price = item.find('figcaption', {'class': 'sc-fb17985a-5 dIWEfZ'}).find('strong',
                                                                                {'class': 'sc-d4956143-2 JDTLz'}).text
        price = int(price.replace('₩', '').replace(',', ''))

        is_sold_out = item.find(text="품절") is not None

        result.append(
            {'itemId': item_id, 'title': title, 'img': img_src, 'url': url, 'price': price,
             'isSoldOut': is_sold_out})

    return result


async def get_albums():
    page = 1
    items = []

    while True:
        url = f"https://shop.weverse.io/ko/shop/GL_KRW/artists/35/categories/615?page={page}"
        page_items = await parse_page(url)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        no_items = soup.find('p', text="등록된 상품이 없습니다.")

        if no_items:
            break

        items.extend(page_items)
        page += 1

    return items
