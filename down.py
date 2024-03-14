import requests

# Открываем файл с ссылками
with open('docs_urls.txt') as file:
    links = file.readlines()

# Последовательно обходим каждую ссылку и скачиваем содержимое
for link in links:
    link = link.strip()  # Удаляем пробелы и символы перевода строки
    response = requests.get(link)

    # Получаем имя файла из ссылки
    filename = link.split("/")[-1]
    if not '.pdf' in filename or not '.zip' in filename:
        filename += '.pdf'

    # Сохраняем содержимое в файл
    with open(filename, 'wb') as file:
        file.write(response.content)
        print(f"Файл {filename} скачан успешно")