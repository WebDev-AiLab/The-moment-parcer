import csv
import logging
from lxml import html
import config
from bs4 import BeautifulSoup
import requests

FILE_CSV_NAME = 'in.csv'



#post-29142 > div.entry-content


with open(FILE_CSV_NAME, mode='r', encoding='utf-8') as read:
            file_reader = csv.reader(read, delimiter=';', quotechar='|')
            for row in file_reader:
                urls = row[0]
                page = requests.get(urls)
                soup = BeautifulSoup(page.text, 'lxml')

                elems = soup.select('body article>.entry-content')[0]
                print(elems)
                