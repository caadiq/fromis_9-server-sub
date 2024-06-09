from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    date: str
    post_number: str


async def get_posts():
    page_number = 1
    all_items = []
    exclude_words = ['디시콘']
    while True:
        url = f"https://gall.dcinside.com/mgallery/board/lists/?id=fromis&exception_mode=recommend&page={page_number}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/124.0.0.0 Whale/3.26.244.21 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        posts = soup.find_all('tr', {'class': 'ub-content us-post'})

        today = datetime.now().strftime('%Y-%m-%d')

        items = []
        for post in posts:
            subject = post.find('td', {'class': 'gall_subject'}).text

            if subject == '일반' or subject == '자료' or subject == '공지' or subject == '컴백가이드':
                date = post.find('td', {'class': 'gall_date'})['title'].split(' ')[0]
                title = post.find('td', {'class': 'gall_tit ub-word'}).find('a').text.strip()
                post_number = post.find('td', {'class': 'gall_num'}).text

                if not any(word in title for word in exclude_words) and date == today:
                    items.append(Item(title=title, date=date, post_number=post_number))

        if not items:
            break

        all_items.extend(items)
        page_number += 1

    return all_items
