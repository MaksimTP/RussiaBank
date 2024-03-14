import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import signal

base_url = "https://www.cbr.ru"
# Загружаем html-страницу
url = 'https://www.cbr.ru/Crosscut/LawActs/Page/94917?Date.Time=Any&Page='  # Замените на адрес нужной веб-страницы

ua = UserAgent()
user_agent = ua.random
headers = {'User-Agent': user_agent}


def handler(signum, frame):
    raise Exception("timeout")

# Устанавливаем таймер на выполнение в течение 3 секунд
signal.signal(signal.SIGALRM, handler)


count_page = 1
count_doc = 1
while(True):
    response = requests.get(url + str(count_page), headers)
    html = response.text

    # Создаем объект Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Находим все внутренние div-элементы
    inner_divs = soup.find_all('div', attrs={'class': 'cross-result'})  # Например, замените 'inner' на нужный вам класс
    with open('docs_urls.txt', 'a') as file:
    # Извлекаем ссылки из внутренних div-элементов
        for div in inner_divs:
            links = div.find_all('a')
            for link in links:
                href = link.get('href')
                if href[0] == '/':
                    print(href)
                    doc_url = base_url + href
                    signal.alarm(10)
                    try:
                        response = requests.get(doc_url, headers)

                        print("sosi")
                        if response.status_code == 200:
                            with open('docs/file' + str(count_doc) + '.pdf', 'wb') as f:
                                f.write(response.content)
                            print('Файл успешно скачан')
                            file.write(doc_url+'\n')
                            count_doc += 1
                        else:
                            print('Ошибка при загрузке:', response.status_code)

                    except Exception as exc:
                        if str(exc) == "timeout":
                            print("Превышено время выполнения")
                        else:
                            print("оШиБкА ЗаПрОсА")
                    signal.alarm(0)


        count_page += 1

