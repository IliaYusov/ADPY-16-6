import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

today = date.today().strftime("%d/%m/%Y")
yesterday = (date.today() - timedelta(1)).strftime("%d/%m/%Y")

ret = requests.get('https://habr.com/ru/all/')
soup = BeautifulSoup(ret.text, 'html.parser')
posts_list = soup.find(name='div', class_='posts_list')
post_previews = posts_list.find_all(name='article', class_='post')
for preview in post_previews:
    title = preview.find(name='a', class_='post__title_link').text
    date = preview.find(name='span', class_='post__time').text.replace('сегодня в', today).replace('вчера в', yesterday)
    link = preview.find(name='a', class_='post__title_link')['href']
    hubs = preview.find(name='ul', class_='post__hubs').text
    preview_text = preview.find(name='div', class_='post__text').text
    post = requests.get(link)
    post_soup = BeautifulSoup(post.text, 'html.parser')
    post_text = post_soup.find(name='div', class_='post__text').text
    for word in KEYWORDS:
        if word in title + hubs + preview_text + post_text:
            print(f'{date} - {title} - {link}')
            break
