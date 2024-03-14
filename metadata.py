# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
#
#
# import datetime
# import os
# import subprocess
# import clickhouse_connect
#
#
# def date_fix(date_bin: str):
#     fix_date = date_bin[4:17]
#     # for sym in replace_syms:
#     #     fix_date = fix_date.replace(sym, "")
#     # fix_date = fix_date.replace('"', "")[0:13]
#     fix_date = datetime.datetime.strptime(fix_date, "%Y%m%d%H%M%S")
#     return str(fix_date)
#
#
# table = "exif"
#
# client = clickhouse_connect.get_client(
#     host="localhost", port=8123, username="default", password=""
# )
#
# client.command(
#     f"CREATE TABLE {table} (id UInt32, document_name String, document_url String, create_date String, modification_date String) ENGINE Memory"
# )
#
# replace_syms = "Db:+'"
#
# id = 1
# # Получаем текущую директорию
# current_directory = os.getcwd()
#
# # Получаем список всех файлов в текущей директории
# files = os.listdir(current_directory)
# print(files)
# file_url = "qqq"
# # Открываем каждый файл с расширением .pdf
# with open("docs_urls.txt", "r") as file_doc_urls:
#     for file in files:
#         if file.endswith(".pdf"):
#             file_url = file_doc_urls.readline().replace("\n", "")
#             file_path = os.path.join(current_directory, file)
#             fp = open(file_path, "rb")
#             parser = PDFParser(fp)
#             doc = PDFDocument(parser)
#             # print(str(doc.info[0]["CreationDate"]))
#             try:
#                 create_date = date_fix(str(doc.info[0]["CreationDate"]))
#             except:
#                 create_date = "none"
#             try:
#                 mod_date = date_fix(str(doc.info[0]["ModDate"]))
#             except:
#                 create_date = "none"
#
#             # for sym in replace_syms:
#             #     create_date = create_date.replace(sym,"")
#             # create_date = create_date.replace('"', "")
#             # create_date = create_date[0:13]
#             # create_date_fix = datetime.datetime.strptime(create_date,"%Y%m%d%H%M%S")
#             print(create_date)
#             print(mod_date)
#             client.insert(
#                 "exif",
#                 [[id, str(file), file_url, create_date, mod_date]],
#                 column_names=[
#                     "id",
#                     "document_name",
#                     "document_url",
#                     "create_date",
#                     "modification_date",
#                 ],
#             )
#             # print(doc.info[0]["ModDate"])
#             id += 1



# from pdfminer.pdfparser import PDFParser
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager
# from pdfminer.layout import LAParams
# from pdfminer.converter import TextConverter
# from io import StringIO
#
# def get_pdf_metadata(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         parser = PDFParser(file)
#         doc = PDFDocument(parser)
#         # metadata = {
#         #     "Title": doc.info[0].get('Title', ''),
#         #     "Author": doc.info[0].get('Author', ''),
#         #     "Subject": doc.info[0].get('Subject', ''),
#         #     "Keywords": doc.info[0].get('Keywords', ''),
#         #     # и так далее
#         # }
#         metadata = doc.info[0]["CreationDate"]
#         return metadata
#
# pdf_path = "docs_new/20240216_in-018-35_12.PDF"
# metadata = get_pdf_metadata(pdf_path)
# print(metadata)
import re

with open("download_info_new.txt", "r") as fp:
    lines = fp.readlines()
    for line in lines:
        if "file_path" in line:
            match = re.search(r'Ссылка: (.*)', line)
            if match:
                link_text = match.group(1)
                print(link_text)