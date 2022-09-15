import datetime
from bs4 import BeautifulSoup
import requests
import csv
import traceback
from json import JSONDecodeError, dumps
from time import sleep

FILE_CSV_NAME = "in.csv"
DIR = 'images'



def post_data(title, content,image):

    link = 'http://127.0.0.1:8000/test' # ссылка на сайт на который всё данные будут поститься

    data = {
    'title' : title,
    'content' : content,
    'image': image
    }

    sleep(1) #добавил таймер на 1 секунду чтобы парсер не уронил сайт 
    response = requests.post(link, json=data)


    print(response, end='\n\n\n')


with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=";", quotechar='|') # Достаём ссылку из файла после чего конвертируем её в строку
    for row in file_reader:
        url = row[0]
        print(row[0])


        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        print("Получаем ссылки")
        try:
            for elem in (soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
                print('Получаем заголовок статьи')
                title = elem.select(".entry-header > h1")
                content = list(elem.select(".entry-content")[0]) # достаю весь контент статьи включая теги после чего закидываю их в список 
                for tag in content: # удаляю теги которые мне не нужны в этом случае все теги которые содержат фотографии
                    if 'itemprop' in str(tag):
                        content.remove(tag)
                clean_content = [str(data) for data in content] #конвертирую все теги в строку чтобы потом мог всё это запушить на бэк
                print("Получаем картинки статьи")
                try:
                    img=elem.find_all('img', src=True, )[0]
                    print('отправка данных', img['src'], end="\n\n")

                    post_data(title[0].text, "".join(clean_content), img['src'])
                except (NameError,ValueError, JSONDecodeError,IndexError ):
                    # В случае если на сайте нету фотографии, фотография будет заменена другой.
                    # ССылка  указана ниже, если она перестанет работать просто замените её
                    # ССылкой на другое фото
                    post_data(title[0].text, "".join(clean_content), 'https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80')


        except Exception as e:
            with open('log.txt', mode='a', encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                file_writer.writerow([f"{traceback.format_exc()}\n", f'date: {datetime.datetime.now}\n\n'])