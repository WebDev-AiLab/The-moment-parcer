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
    random_image_url = []

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
            'title': self.title,
            'content': self.content,
            'image': str(self.image).strip("['']"),
            'img_list': self.image_list
        }
        response = requests.post(self.link, json=context)
        print(response.json(), response.status_code)

    def clean_title(self):
        """
        ООП МЕТОД #2: Используется для того чтобы очистить заголовок от не нужных фраз
        param to_delete: Содержит список фраз которые должны удалиться из заголовка
        """
        to_delete = ['- TUDAY.ru', '- Фейков нет', '- WorkingHard', '- KZNPORTAL.RU', '- Shturmuy.ru', '- Уроки по Lightroom и Photoshop']
        self.title = str(self.title).strip("['']")
        for item in to_delete:
            if item in self.title:
                self.title = self.title.replace(item, '')

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
            print(image_tag)
            image_link = str(image_tag['src'])
            delete_image = '//assets.pinterest.com/images/pidgets/pinit_fg_en_rect_red_28.png'
            if delete_image not in image_link:
                if requests.get(image_link):
                    self.image_list.append(image_link)
                else:
                    self.image_list.append(choice(self.random_image_url))

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
        for tag in content:
            for delete in ['box fact clearfix', 'toc empty', 'data-pin-do=']:
                if delete in str(tag):
                    content.remove(tag)
        self.content = [str(data) for data in content if data != str]

        # проверка ссылки превью фотографии
        if len(self.image) == 0:
            with open('url_image.csv', 'r', newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for rows in file_reader:
                    self.random_image_url.append(rows[0])
                self.image = choice(self.random_image_url)

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
                    self.clean_title()
                    self.request_post()
                    self.image_list.clear()

        except Exception as error:
            logging.warning(error)
