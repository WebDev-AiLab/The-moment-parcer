from bs4 import BeautifulSoup
import requests
import os
import random
import csv
import uuid
import traceback
from datetime import date


today = date.today()

def download_images(imagelinks):
    # проверка на наличие папки images
    if not os.path.exists("images"):
        os.mkdir("images")

    imagename = 'images/' + str(uuid.uuid4()) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(page.content)
    # Записываем данные в csv
    # открываем csv-файл
    with open('out.csv', mode='a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([f"{title[0].text}", f"{text[0].text}", f"{imagename}"])



FILE_CSV_NAME = "in.csv"
with open(FILE_CSV_NAME, encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter = ";")
    for row in file_reader:
        url_page = row[0]
        print(url_page)

# Получаем адрес страницы
page = requests.get(f'{(str(url_page))}')
soup = BeautifulSoup(page.text, 'lxml')

print("Получаем ссылки")


#заходим в каждый "отдел" где посты рассортированы по месяцам

try:
    for elem in (soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
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


        print(f"все данные взяты с данной страниы {url_page}\n\n")
except Exception as e:
    print(traceback.format_exc())
    with open('log.txt', mode='a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([f"{traceback.format_exc()}\n", f'date: {today}\n\n'])
