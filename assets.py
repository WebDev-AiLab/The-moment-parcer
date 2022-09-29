import csv
import random

from bs4 import BeautifulSoup
import logging
import config
import requests


class Parser():
    def __init__(self, link, FILE_CSV_NAME):
        self.link = link
        self.FILE_CSV_NAME = FILE_CSV_NAME

    def request_post(self, title, content, image, img_list):
        """
        ООП МЕТОД #1: Содержит атрибуты инициатора для post запроса в сайт
        :param title: Заголовок
        :param content: Содержимое поста
        :param image: Миниатюра
        :param img_list: Список фото из поста
        :return:
        """
        context = {
            'title': title,
            'content': content,
            'image': image,
            'img_list': img_list
        }
        response = requests.post(self.link, json=context)
        return response.status_code

    def open_file(self):
        """
        ООП МЕТОД #2:
            Тут мы открываем файл in.csv и пошагово разбираем статью
            затем с помощью ООП МЕТОДА #1 делаем post запрос с контекстными данными
         """
        try:
            with open(self.FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
                file_reader = csv.reader(read, delimiter=';', quotechar='|')
                for row in file_reader:
                    urls = row[0]
                    page = requests.get(urls)
                    soup = BeautifulSoup(page.text, 'lxml')
                    logging.info('Get link: {}'.format(urls))
                    try:
                        for element in (soup.select(".site-content > .site-content-inner > .content-area > .site-main "
                                                    "> article")):
                            title = element.select(".entry-title > h1")
                            print(title)
                            content = list(element.select(".entry-content")[0])
                            logging.info('We take the content of the post with the title: {}'.format(title))
                            for tag in content:
                                for delete in ['box fact clearfix', 'toc empty', ]:
                                    if delete in str(tag):
                                        content.remove(tag)
                            clean_content = [str(data) for data in content]
                            logging.info("Getting the post thumbnail image")
                            try:
                                img_list = []
                                img = element.find_all('img', src=True, )
                                for i in img:
                                    img_list.append(i['src'])
                                self.request_post(title[0].text,
                                                  "".join(clean_content),
                                                  img[0]['src'],
                                                  img_list)
                            except Exception as error:
                                logging.critical(error)
                                with open('url_image.csv', 'r', newline='') as csvfile:
                                    spam_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                                    url_image_moment = []
                                    for rows in spam_reader:
                                        url_image_moment.append(rows)
                                self.request_post(title[0].text, "".join(clean_content),
                                                  random.choice(url_image_moment)[0],
                                                  img_list)
                    except Exception as error:
                        logging.critical(f"Critical error: {error}")

        except Exception as error:
            logging.critical(error)
