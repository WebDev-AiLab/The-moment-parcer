from bs4 import BeautifulSoup
import requests
import os

n = 1
max_page = 2


def download_images(imagelinks):
    # проверка на наличие папки images
    if not os.path.exists("images"):
        os.mkdir("images")

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

    imagename = 'images/' + str(i+1) + '.jpg'
    with open(imagename, 'wb') as file:
        file.write(response.content)

# Check connect
# print(page.status_code)


while n < max_page:
    # Получаем адрес страниц
    url = f'https://the-moment.ru/page/{n}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    print("Получаем ссылки")
    for el in soup.select(".post-card "):
    # Получаем url страниц
        for url in soup.find_all('a', href=True):
            url_a = url['href']
            # Скипаем все категории ( по длине )
            if len(url_a) <= 49:
                pass
            else:
                # Парсим отдельную страницу
                single_post_url = url_a
                single_post_page = requests.get(single_post_url)
                single_post_soup = BeautifulSoup(single_post_page.text, 'lxml')
                # Получаем заголовок
                for elem in (single_post_soup.select(".site-content > .site-content-inner > .content-area > .site-main > article")):
                    print('Получаем заголовок статьи')
                    title = elem.select(".entry-header > h1")
                    print(title[0].text)
                    # получаем текст статьи
                    print('Получаем текст статьи')
                    text = elem.select(".entry-content")
                    print(text[0].text)
                    # Получаем картинки
                    print("Получаем картинки статьи")
                    for img in single_post_soup.find_all('img', src=True):
                        print("rer")
                        img_url = img['src']
                        print(img_url)
                        if img_url == "https://the-moment.ru/wp-content/uploads/2018/10/shapka_sayta_35.png":
                            pass

                        else:
                            print(img_url)
                            imagelinks = []
                            #
                            # for img in soup.find_all('img', src=True, ):
                            #     imagelinks.append(img_url)
                            #     download_images(imagelinks)
                        break
                print(url_a)

    print("Получаем картинки с главной страницы")
    for img in soup.find_all('img', src=True):
        img_url = img['src']
        if img_url == "https://the-moment.ru/wp-content/uploads/2018/10/shapka_sayta_35.png":
            pass
        else:
            print(img_url)
            imagelinks = []
            for img in soup.find_all('img', src=True, ):
                imagelinks.append(img_url)
                download_images(imagelinks)

    n += 1
