from bs4 import BeautifulSoup
import requests
import os

n = 1
max_page = 2

# Check connect
# print(page.status_code)

def download_images(imagelinks):
    #проверка на наличие папки images
    if not os.path.exists("images"):
        os.mkdir("images")
    

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

    imagename =  'images/' + str(i+1) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(response.content) 


while n < max_page:
    # Получаем адрес страниц
    url = f'https://the-moment.ru/page/{n}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Получаем ссылки все сыылки на статьи на странице
    for a in soup.find_all('a', href=True):
        print(a['href'])

    # Получаем ссылки на картинки со страние со всеми статьями
    imagelinks = []
    for img in soup.find_all('img', src=True,):
        imagelinks.append(img['src'])
        download_images(imagelinks)

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