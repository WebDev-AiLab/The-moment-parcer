import csv
import logging
from lxml import html
import config
from bs4 import BeautifulSoup
import requests

FILE_CSV_NAME = 'in.csv'

link = 'http://127.0.0.1:8000/create'



def get_images(soup):
    content_box = soup.xpath('//span[@itemprop="image"]')
    image_list = []
    for image_tag in content_box:
        image = image_tag.xpath('.//img[@src]/@src')[0]
        image_list.append(image)
    return image_list


def find_data(lxml, soup):
    title = lxml.xpath('/html/head/title/text()')
    elems = soup.select('body article>.entry-content')[0]
    image = lxml.xpath('/html/head/meta[@property="og:image"]/@content')
    content_box = lxml.xpath('//span[@itemprop="image"]')
    image_list = []

    for image_tag in content_box:
        image = image_tag.xpath('.//img[@src]/@src')[0]
        image_list.append(image)
    
    context = {
        'title': str(title).strip("['']"),
        'content': str(elems).strip("['']"),
        'image': str(image).strip("['']"),
        'img_list' : image_list
    }
    print(context)
    response = requests.post(link, json=context)
    return response.status_code


def parser():
    
        with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
            file_reader = csv.reader(read, delimiter=';', quotechar='|')
            for row in file_reader:
                urls = row[0]
                page = requests.get(urls)
                lxml = html.fromstring(page.content)
                soup = BeautifulSoup(page.text, 'lxml')
                logging.info('Get link: {}'.format(urls))
                find_data(lxml, soup)


parser()