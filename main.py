from bs4 import BeautifulSoup
import requests
import os



def download_images(imagelinks):
    # проверка на наличие папки images
    if not os.path.exists("images"):
        os.mkdir("images")

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

    imagename = 'images/' + str(i+1) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(response.content)


# Получаем адрес страницы 
page = requests.get(f'https://the-moment.ru/sitemap.html')
soup = BeautifulSoup(page.text, 'lxml')

print("Получаем ссылки")

#заходим в каждый "отдел" где посты рассортированы по месяцам
for posts_in_month in soup.select('td > a')[1::]:
    response = requests.get(posts_in_month['href'])
    soup = BeautifulSoup(response.text, 'lxml')

    #вытаскиваем пост из каждого месяца
    for post in soup.select('td > a'):
        print(f"{post['href']}\n\n")



        #всё что находится ниже надо доработать 
        for elem in (single_post_soup.select(".site-content > .site-content-inner > .content-area > .site-main > article > .post-cards post-cards--grid")):
            print('Получаем заголовок статьи')
            title = elem.select(".entry-header > h1")
            print(title[0].text)
            # получаем текст статьи
            print('Получаем текст статьи')
            text = elem.select(".entry-content")
            print(text[0].text)
            # Получаем картинки
            print("Получаем картинки статьи")

            imagelinks = []
            for img in single_post_soup.find_all('img', src=True, ):
                print(img['src'])

                imagelinks.append(img['src'])
                download_images(imagelinks)
        print(f'все данные взяты с данной страниы {single_post_url}')