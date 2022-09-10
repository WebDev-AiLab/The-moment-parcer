import datetime
from bs4 import BeautifulSoup
import requests
import csv
import traceback


FILE_CSV_NAME = "in.csv"
DIR = 'images'



def post_data(title, content,image):
    link = 'http://127.0.0.1:8000/test'

    data = {
    'title' : title,
    'content' : content,
    'image': image
    }

    response = requests.post(link, json=data)
    print(response, response.json())
with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter=";", quotechar='|')
    for row in file_reader:
        url = row[0]
        print(row[0])


        page = requests.get(f'{(str(url))}')
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
                try:
                    for elem in (post_soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
                        print('Получаем заголовок статьи')
                        title = elem.select(".entry-header > h1")
                        # print(f'{title[0].text}\n\n')

                        # print('Получаем текст статьи')
                        text = elem.select(".entry-content")
                        # print(f"{text[0].text}\n\n")

                        print("Получаем картинки статьи")
                        try:
                            for img in elem.find_all('img', src=True, ):
                                print(f"{img['src']}\n\n")
                            
                        except NameError:
                            post_data(title[0].text, text[0].text, 'shorturl.at/cnuQS')

                        else:
                            print('отправка данных', img['src'], end="\n\n\n")
                            post_data(title[0].text, text[0].text, img['src'])


                except Exception as e:
                    print(traceback.format_exc())
                    with open('log.txt', mode='a', encoding='utf-8') as w_file:
                        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
                        file_writer.writerow([f"{traceback.format_exc()}\n", f'date: {datetime.datetime.now}\n\n'])