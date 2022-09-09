from bs4 import BeautifulSoup
import requests
import os
import random
import csv


def download_images(imagelinks):
    # проверка на наличие папки images
    if not os.path.exists("images"):
        os.mkdir("images")

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

    imagename = 'images/' + str(i+1) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(response.content)

    # Записываем данные в csv
    # открываем csv-файл
    with open('out.csv', mode='a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([f"{title[0].text}", f"{text[0].text}", f"{imagename}"])


# Получаем адрес страницы
page = requests.get(f'https://the-moment.ru/sitemap.html')
soup = BeautifulSoup(page.text, 'lxml')

print("Получаем ссылки")


#заходим в каждый "отдел" где посты рассортированы по месяцам
for posts_in_month in soup.select('td > a')[1::]:
    response = requests.get(posts_in_month['href'])
    soup = BeautifulSoup(response.text, 'lxml')

    #вытаскиваем пост из каждого месяца
    for post in soup.select('td > a'):
        post_page = requests.get(post['href'])
        post_soup = BeautifulSoup(post_page.text, 'lxml')
        print(f"{post['href']}\n\n")
        # print(post_soup)

        for elem in (post_soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
            print('Получаем заголовок статьи')
            title = elem.select(".entry-header > h1")
            print(f'{title[0].text}\n\n')

            print('Получаем текст статьи')
            text = elem.select(".entry-content")
            print(f"{text[0].text}\n\n")

            print("Получаем картинки статьи")

            imagelinks = []
            for img in elem.find_all('img', src=True, ):
                print(f"{img['src']}\n\n")
                # Если нет картинки
                if len(img['src']) < 1:
                    # Открываем папку с готовым картинками
                    # Открываем папку с картинками
                    path = r"random_img"
                    # Папка где хранятся картинки к статьям
                    DIR = 'images'
                    # Выбраем случайную картинку
                    filename = random.choice([
                        x for x in os.listdir(path)
                        if os.path.isfile(os.path.join(path, x))
                    ])
                    # Перемещаем её в папку с основными картинками
                    os.replace(f"random_img/{filename}", f"images/{filename}")
                    # Открываем и записываем данные в csv
                    with open('out.csv', mode='a', encoding='utf-8') as w_file:
                        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                        file_writer.writerow([f"{title[0].text}", f"{text[0].text}", f"{filename}"])
                else:
                    imagelinks.append(img['src'])
                    download_images(imagelinks)

        print(f"все данные взяты с данной страниы {post['href']}\n\n")
