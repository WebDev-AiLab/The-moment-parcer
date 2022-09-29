import csv
import logging
from lxml import html
import config
import bs4
import requests

FILE_CSV_NAME = 'in.csv'


def parser():
    try:
        with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
            file_reader = csv.reader(read, delimiter=';', quotechar='|')
            for row in file_reader:
                urls = row[0]
                page = requests.get(urls)
                soup = html.fromstring(page.content)
                logging.info('Get link: {}'.format(urls))
                title = soup.xpath('/html/head/title/text()')
                content = soup.xpath('/html/body/div[1]/div[4]/div/div[1]/main/article/div[3]/p/text()')
                image = soup.xpath('/html/head/meta[@property="og:image"]/@content')
                context = {
                    'title': str(title).strip("['']"),
                    'content': str(content).strip("['']"),
                    'image': str(image).strip("['']")
                }
                print(context)
    except Exception as error:
        logging.warning(error)
parser()