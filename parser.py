import csv
import logging
from lxml import html
import config
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
FILE_CSV_NAME = 'in.csv'

link = 'https://my-tips.ru/create'

context = {
    'image': 'https://workinghard.ru/wp-content/uploads/2020/12/25-priznakov-uspekha-2-1024x597.jpg',
    'title': 'sdasdsdasdasda',
    'content': 'asdasdasdasdasda',
    'slug': 'ssdfsdfsdfsdfsdfsdf'
}
a = requests.post(link, context)
print(a)