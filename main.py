import datetime
from bs4 import BeautifulSoup
import requests
import csv
import traceback
from json import JSONDecodeError, dumps
from time import sleep
import random
import os

FILE_CSV_NAME = "in.csv"
DIR = 'images'



def post_data(title, content, image, ):

    link = 'https://my-tips.ru/test' # ссылка на сайт на который всё данные будут поститься

    data = {
    'title' : title,
    'content' : content,
    'image': image,

    }
    # sleep(1) #добавил таймер на 1 секунду чтобы парсер не уронил сайт
    with open('out.csv', 'a+', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([f"{data} \n\n\n"])

    response = requests.post(link, json=data)

    print(response, response.json(), end='\n\n\n')


with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=";", quotechar='|') # Достаём ссылку из файла после чего конвертируем её в строку
    for row in file_reader:
        url = row[0]
        print(row[0])


        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        print("Получаем ссылки")
        print(url)
        try:
            for elem in (soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
                print('Получаем заголовок статьи')
                title = elem.select(".entry-header > h1")

                content = list(elem.select(".entry-content")[0]) # достаю весь контент статьи включая теги после чего закидываю их в список
                for tag in content: # удаляю теги которые мне не нужны в этом случае все теги которые содержат фотографии
                    for i in ['table-of-contents open', 'box fact clearfix', 'toc empty', 'a href=']:
                        if i in str(tag):
                            content.remove(tag)


                clean_content = [str(data) for data in content] #конвертирую все теги в строку чтобы потом мог всё это запушить на бэк
                
                print("Получаем картинки статьи")


                try:
                    img=elem.find_all('img', src=True, )[0]
                    print('отправка данных', img['src'], end="\n\n")
                    print(img['src'])
                    post_data(title[0].text, "".join(clean_content), img['src'], )
                except (NameError,ValueError, JSONDecodeError,IndexError ):
                    # В случае если на сайте нету фотографии, фотография будет заменена другой.
                    # ССылка  указана ниже, если она перестанет работать просто замените её
                    # ССылкой на другое фото
                    path = r"images"
                    filename = random.choice([
                        x for x in os.listdir(path)
                        if os.path.isfile(os.path.join(path, x))
                    ])
                    with open('url_image.csv', 'r', newline='') as csvfile:
                        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                        url_image_moment = []
                        for row in spamreader:
                            url_image_moment.append(row)
                        
                    post_data(title[0].text, "".join(clean_content), random.choice(url_image_moment),  )


        except Exception as e:
            with open('log.txt', mode='a', encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                file_writer.writerow([f"{traceback.format_exc()}\n", f'page: {url}\n\n'])