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
    link = 'http://127.0.0.1:8000/test'

    data = {
    'title' : title,
    'content' : content,
    'image': image
    }
    sleep(1)
    response = requests.post(link, json=data)


    print(response, response.json())


with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter=";", quotechar='|')
    for row in file_reader:
        url = row[0]
        print(row[0])
        # Получаем адрес страницы
        page = requests.get(f'{(str(url))}')
        soup = BeautifulSoup(page.text, 'lxml')
        # print(soup)
        print("Получаем ссылки")
        try:
            for elem in (soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
                print('Получаем заголовок статьи')
                title = elem.select(".entry-header > h1")
                # print(f'{title[0].text}\n\n')

                # print('Получаем текст статьи')
                content = list(elem.select(".entry-content")[0]) # достаю весь контент статьи включая теги
                print(content)
                # print(type(content),content, end='\n\n\n')

                # print(content)
                for tag in content:
                    # print(tag, end='\n\n')
                    if 'itemprop' in str(tag):
                        content.remove(tag) # удаляю теги которые мне не нужны 
                
                print("{}".join(content)) # пытаюсь запихнуть все данные в списке в строку но выдаёт ошибку 



                print("Получаем картинки статьи")
                try:
                    img=elem.find_all('img', src=True, )[0]
                    print('отправка данных', img['src'], end="\n\n")

                    # post_data(title[0].text, "".join(content), img['src'])

                except (NameError,ValueError, JSONDecodeError,IndexError ):
                    post_data(title[0].text, content, 'https://images.unsplash.com/photo-1551218808-94e220e084d2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80')


        except Exception as e:
            print(traceback.format_exc())
            with open('log.txt', mode='a', encoding='utf-8') as w_file:
                file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                file_writer.writerow([f"{traceback.format_exc()}\n", f'date: {datetime.datetime.now}\n\n'])