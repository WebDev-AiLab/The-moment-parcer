from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from random import choice
from lxml import html
from bs4 import BeautifulSoup
import logging
import config
import requests
import csv


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

    def request_post(self, ):
        """
        ООП МЕТОД #1: Содержит атрибуты инициатора для post запроса в сайт
        :param title: Заголовок
        :param content: Содержимое поста
        :param image: Миниатюра
        :param img_list: Список фото из поста
        :return:
        """
        print(self.image_list)
        context = {
            'title': str(self.title).strip("['']"),
            'content': self.content,
            'image': str(self.image).strip("['']"),
            'img_list': self.image_list
        }

        response = requests.post(self.link, json=context)
        print(response.status_code)

    def get_images(self, ):
        """
        ООП МЕТОД #2: Используется для нахождения фотографий в статье
                      Если на сайте нету фотографии, то функция не сработает
        :param content: Содержит элементы html в котором находятся фотографии
        :param image_list: Переменная класса которая содержит список фотографий(ссылки)
        """
        content = self.soup
        image_list = content[0].find_all('img', src=True)
        for image_tag in image_list:
            image_link = str(image_tag['src'])
            delete_image = '//assets.pinterest.com/images/pidgets/pinit_fg_en_rect_red_28.png'
            if delete_image not in image_link:
                self.image_list.append(image_link)

    def get_data(self):
        """
        ООП МЕТОД #3:
            Тут мы находим нужные данные на сайте после чего сохраняем их
            В переменной класса для дальнейшего использования 
            Если на сайте, нету превью фотографии, то фотография достаётся из
            Файла url_image.csv
        param content: Переменная которая содержит контент статьи включая html элементы
        param image_url: Перменная которая содержит ссылки на одну из фотографий которые
        находятся в файле url_image.csv. 
         """
        self.title = self.lxml.xpath('/html/head/title/text()')[0]
        self.image = self.lxml.xpath('/html/head/meta[@property="og:image"]/@content')
        self.soup = self.soup.select('body article>.entry-content')
        content = list(self.soup[0])
        print(content, end='\n\n\n\n\n')
        for tag in content:
            for delete in ['box fact clearfix', 'toc empty', 'data-pin-do=', ]:
                if delete in str(tag):
                    content.remove(tag)
        print(content)
        self.content = [str(data) for data in content if data != str]

        # проверка ссылки фотографии
        if len(self.image) == 0:
            with open('url_image.csv', 'r', newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                image_url = []
                for rows in file_reader:
                    image_url.append(rows[0])
                self.image = choice(image_url)

    def open_file(self):
        """
        ООП МЕТОД #4:
            Тут мы открываем файл in.csv и пошагово разбираем статью
            затем с помощью ООП МЕТОДА #1 делаем post запрос с контекстными данными
         """
        disable_warnings(InsecureRequestWarning)
        try:
            with open(self.FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
                file_reader = csv.reader(read, delimiter=';', quotechar='|')
                for row in file_reader:
                    urls = row[0]
                    page = requests.get(urls, verify=False)
                    self.lxml = html.fromstring(page.content)
                    self.soup = BeautifulSoup(page.text, 'lxml')
                    logging.info('Get link: {}'.format(urls))
                    self.get_data()
                    self.get_images()
                    self.request_post()
                    self.image_list.clear()

        except Exception as error:
            raise error
            logging.warning(error)
