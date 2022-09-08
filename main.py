from bs4 import BeautifulSoup
import requests

n = 1
max_page = 5

# Check connect
# print(page.status_code)

while n < max_page:
    # Получаем адрес страниц
    url = f'https://the-moment.ru/page/{n}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Получаем ссылки все сыылки на статьи на странице
    for a in soup.find_all('a', href=True):
        print(a['href'])

    # Получаем ссылки на картинки со страние со всеми статьями
    for img in soup.find_all('img', src=True):
        print(img['src'])

    for el in soup.select(".post-card "):
        # Получаем заголовки со страницы
        title = el.select(".post-card__title > span > a")
        # url_a = el.select(".post-card__title > span")

        print(title[0].text)
    n += 1

    # img = el.select(".post-card__thumbnail > a")
    # article = el.select(".articleBody")
    # print(article)
    # print(img)
    # print(title[0].text)