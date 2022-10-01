import csv
import random
from lxml import html
from bs4 import BeautifulSoup
import logging
import config
import requests


class Parser():

    lxml = ""
    soup = ""
    title = ""
    content = ""
    image = ""
    image_list = []


    def __init__(self, link, FILE_CSV_NAME):
        self.link = link
        self.FILE_CSV_NAME = FILE_CSV_NAME




    def request_post(self,):
        """
        ООП МЕТОД #1: Содержит атрибуты инициатора для post запроса в сайт
        :param title: Заголовок
        :param content: Содержимое поста
        :param image: Миниатюра
        :param img_list: Список фото из поста
        :return:
        """
        context = {
            'title': str(self.title[0]).strip("['']"),
            'content': "".join(self.content),
            'image': str(self.image[0].strip("['']")),
            'img_list': self.image_list
        }

        response = requests.post(self.link, json=context)
        return response.status_code


    def get_images(self,):
        """
        ООП МЕТОД #2: Используется для нахождения фотографий в статье
        :param content: Содержит элементы html в котором находятся фотографии
        """

        content = self.lxml.xpath('//span[@itemprop="image"]')
        for image_tag in content:
             self.image_list.append(image_tag.xpath('.//img[@src]/@src')[0])


    def get_data(self):
        """
        ООП МЕТОД #3:
            Тут мы находим нужные данные на сайте после чего сохраняем их
            В переменной класса для дальнейшего использования 
         """
        self.title = self.lxml.xpath('/html/head/title/text()')
        self.image = self.lxml.xpath('/html/head/meta[@property="og:image"]/@content')
        content = list(self.soup.select('body article>.entry-content')[0])

        for tag in content:
            for delete in ['box fact clearfix', 'toc empty', ]:
                if delete in str(tag):
                    content.remove(tag)

        self.content = [str(data) for data in content if data != str]


    def open_file(self):
        """
        ООП МЕТОД #4:
            Тут мы открываем файл in.csv и пошагово разбираем статью
            затем с помощью ООП МЕТОДА #1 делаем post запрос с контекстными данными
         """
        try:
            with open(self.FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
                file_reader = csv.reader(read, delimiter=';', quotechar='|')
                for row in file_reader:
                    urls = row[0]
                    page = requests.get(urls)
                    self.lxml = html.fromstring(page.content)
                    self.soup = BeautifulSoup(page.text, 'lxml')
                    logging.info('Get link: {}'.format(urls))
                    self.get_data()
                    self.get_images()
                    self.request_post()
                    self.image_list.clear()

        except Exception as error:
            logging.warning(error)
