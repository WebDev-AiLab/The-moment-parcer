from bs4 import BeautifulSoup
import requests

n = 1

max_page = 2  # Максимальное число страниц сайта

# Check connect
# print(page.status_code)

while n < max_page:
    # Получаем адрес страниц
    url = f'https://the-moment.ru/page/{n}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')


    # Получаем ссылки на картинки со страние со всеми статьями
    for img in soup.find_all('img', src=True):

        img_url = img['src']
        #
        if img_url == "https://the-moment.ru/wp-content/uploads/2018/10/shapka_sayta_35.png":
            pass
        else:
            print(img_url)

    # Получаем ссылки все сыылки на статьи на странице
    for a in soup.find_all('a', href=True):
        # Получаем одиночную ссылку на статью
        single_article_url = a['href']
        # Открываем страницу статьи
        try:
            solo_page = requests.get(single_article_url)
            soup_single_article = BeautifulSoup(solo_page.text, 'lxml')



            # for el in soup.select(".post-card "):
            #     # Получаем заголовки со страницы
            #     title = el.select(".post-card__title > span > a")
            #     print(title[0].text)

            # solo_page_title = soup_single_article.select(".entry-header > h1")
            # print(solo_page_title[0].text)
            # Береём описание со страницы
            # for el in soup_single_article.select(".entry-content"):
            #     # Получаем заголовки со страницы
            #     desc = el.select("p")
            #     print(desc[0].text)
            # print(soup_single_article)
        # Если ошибка пропускаем её
        except:
            continue
        # print(single_article_url)




    #
    n += 1