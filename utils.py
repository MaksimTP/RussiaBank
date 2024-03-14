import datetime
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
import re


def date_fix(date_bin: str):
    """
    Функция date_fix преобразует бинарное представление даты в строку формата '%Y-%m-%d %H:%M:%S'.

    Параметры:
    - date_bin: строка с бинарным представлением даты

    Возвращаемое значение:
    str: строка с преобразованной датой в формате '%Y-%m-%d %H:%M:%S'
    """
    fix_date = date_bin[4:17]
    fix_date = datetime.datetime.strptime(fix_date, "%Y%m%d%H%M%S")
    return str(fix_date)


def get_metadata(file_path):
    """
    Функция get_metadata извлекает метаданные из PDF-файла.

    Параметры:
    - file_path: путь к PDF-файлу

    Возвращаемое значение:
    - список, содержащий дату создания и дату модификации файла
    """
    file_path = "docs_new/" + file_path
    with open(file_path, "rb") as fp:
        # enc = chardet.detect(text).get("encoding")
        try:
            parser = PDFParser(fp)
        except:
            return ["None", "None"]
        doc = PDFDocument(parser)
        try:
            create_date = date_fix(str(doc.info[0]["CreationDate"]))
        except:
            create_date = "none"
        try:
            mod_date = date_fix(str(doc.info[0]["ModDate"]))
        except:
            create_date = "none"
    return [create_date, mod_date]


def get_link(file_path):
    """
    Функция get_link извлекает ссылку из файла download_info_new.txt по заданному пути к файлу.

    Параметры:
    - file_path: str, путь к файлу

    Возвращаемое значение:
    - str, текст ссылки
    """
    with open("download_info_new.txt", "r") as fp:
        lines = fp.readlines()
        for line in lines:
            if file_path in line:
                match = re.search(r"Ссылка: (.*)", line)
                if match:
                    link_text = match.group(1)
                    return link_text
