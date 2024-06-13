from datetime import datetime

import requests
from bs4 import BeautifulSoup


async def get_posts():
    items = []
    exclude_words = ['디시콘']

    url = f"https://gall.dcinside.com/mgallery/board/lists/?id=fromis&exception_mode=recommend"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Whale/3.26.244.21 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('tr', {'class': 'ub-content us-post'})

    for post in posts:
        subject = post.find('td', {'class': 'gall_subject'}).text

        if subject == '일반' or subject == '자료' or subject == '공지' or subject == '컴백가이드':
            date_element = post.find('td', {'class': 'gall_date'})
            date_string = date_element['title']
            datetime_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            date = datetime_obj.isoformat()
            title = post.find('td', {'class': 'gall_tit ub-word'}).find('a').text.strip()
            post_id = int(post.find('td', {'class': 'gall_num'}).text)
            url = "https://gall.dcinside.com/mgallery/board/view/?id=fromis&no=" + str(post_id)

            if not any(word in title for word in exclude_words):
                items.append({"postId": post_id, "title": title, "url": url, "date": date})

    return items
