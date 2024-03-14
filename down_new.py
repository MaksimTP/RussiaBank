import requests
import os
from urllib.parse import unquote
import re
from requests.exceptions import MissingSchema


with open("download_info.txt", "w") as info_file:
    # Открываем файл с ссылками
    with open("docs_urls.txt") as file:
        links = file.readlines()

    # Последовательно обходим каждую ссылку и скачиваем содержимое
    for link in links:
        try:
            link = link.strip()  # Удаляем пробелы и символы перевода строки

            # Отправляем HEAD запрос для получения информации о файле
            response = requests.head(link)

            # Если сервер поддерживает заголовок Content-Disposition, получаем имя файла из него
            if "Content-Disposition" in response.headers:
                header = response.headers["Content-Disposition"]
                filename = re.findall(
                    r'filename\*?=\"?([^\";]*)\"?(;filename\*?=UTF-8\'\'([^"]*))?',
                    header,
                )
                if filename:
                    filename = filename[0][0].strip()
                else:
                    filename = re.findall("filename=(.*)", header)[0].strip()
                filename = unquote(filename)

            # В противном случае извлекаем имя файла из URL
            else:
                filename = os.path.basename(unquote(requests.utils.urlparse(link).path))

            # Отправляем GET запрос для скачивания файла
            response = requests.get(link)
            if response.status_code == 200:  # Проверяем успешность запроса
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"Файл {filename} скачан успешно")
                info_file.write(f"Файл: {filename}, Ссылка: {link}\n")
            else:
                print(f"Не удалось скачать файл {filename}")
        except MissingSchema:
            print(f"Неверная ссылка: {link}. Пропущено.")
