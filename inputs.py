
import clickhouse_connect
import subprocess
import os
from pdfreader import SimplePDFViewer

def set_to_master(client, id, id_doc, chunk):
    client.insert('ML_unitaz', [id, id_doc, chunk], column_names=['id', 'id_document', 'chunk'])

def set_to_slave(client, id, document_name, document_url):
    client.insert('ML_skibidi', [id, document_name, document_url], column_names=['id', 'document_name', 'document_url'])

def set_to_db(client,id, id_doc, chunk,document_name, document_url):
    set_to_master(client, id, id_doc, chunk)
    set_to_slave(client, id, document_name, document_url)


def get_chunk(client, table, id):
    arr_chunk = client.query(f'SELECT chunk FROM {table} WHERE id = {id}')
    return arr_chunk.result_rows[0][0]


def get_row(client, id):
    data1 = client.query(f'SELECT * EXCEPT (id) FROM ML_skibidi WHERE id = {id}')
    data2 = client.query(f'SELECT * EXCEPT (id) FROM ML_unitaz WHERE id = {id}')
    if data1 != None and data2 != None:
        result = data1.result_rows[0] + (data2.result_rows[0])
        return result
    else:
        return None

client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='')

table = "document"
table2 = "chunk"


# set_to_master(client, 1,1,[1,2,3,4,5,6,7,8,9,10])
row1 = [1000, 'String Value 1000', "5.233"]
row2 = [2000, 'String Value 2000', "-"]
data = [row1]
# client.insert('new_table', data, column_names=['key', 'value', 'metric'])
# print(len(data[0]))
client.insert('ML_skibidi', data, column_names=['id', 'document_name', 'document_url'])
#
# client.command(f'CREATE TABLE {table} (id UInt32, document_name String, document_url String) ENGINE MergeTree PRIMARY KEY id')
#
# client.command(f'CREATE TABLE {table2} (id UInt32, id_chunk UInt32, chunk Array(Float32)) ENGINE MergeTree ORDER BY id_document')
#
#
# import subprocess
# import os
# from pdfreader import SimplePDFViewer
# from sentence_transformers import SentenceTransformer
#
# class DocumentHolder:
#     try:
#         os.mkdir("docs")
#     except:
#         pass
#
#     N = len(os.listdir("docs"))
#
#     def __init__(self, url) -> None:
#         self.url = url
#         self.text = {}
#         self.load_doc()
#         self.read_file()
#
#     def load_doc(self):
#         try:
#             subprocess.call(f"curl -o docs/{self.N}.pdf {self.url}", shell=True, executable="/bin/bash")
#             self.filename = f"{self.N}.pdf"
#             self.N += 1
#         except Exception as ex:
#             print(ex)
#
#     def read_file(self):
#         self.fd = open("docs/" + self.filename,  "rb")
#         self.viewer = SimplePDFViewer(self.fd)
#
#         cnt = 1
#         for canvas in self.viewer:
#             self.text[cnt] = "".join(canvas.strings)
#             cnt += 1
#
#
# import numpy as np
#
# # def get_detailed_instruct(query: str, task_description: str = 'Given a web search query, retrieve relevant passages that answer the query') -> str:
# #     return f'Instruct: {task_description}\nQuery: {query}'
#
# class Encoder:
#     def __init__(self, text_by_pages: dict[int,str], document_name: str = "", chunk_size: int = 1) -> None:
#         self.text_by_pages = text_by_pages
#         self.document_name = document_name
#         self.chunk_size = chunk_size
#         self.encoded_text_by_pages = text_by_pages.copy()
#         self.model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')
#
#     def encode_document(self):
#         for page_key in self.text_by_pages:
#             chunk = ""
#             for i in range(self.chunk_size):
#                 chunk += self.text_by_pages.get(page_key + i, "")
#             embedding = self.model.encode(chunk, normalize_embeddings=True)
#             self.encoded_text_by_pages[page_key] = embedding
#         return self.encoded_text_by_pages
#
#     def encode_query(self, query: str):
#         return self.model.encode(query)
# #content > div > div > div > div.cross-results > div:nth-child(1) > div.title-source.offset-md-4 > div.title
# #content > div > div > div > div.cross-results > div:nth-child(2) > div.title-source.offset-md-4 > div.title > span > a > span:nth-child(1)
# urls = ["https://www.cbr.ru/Crosscut/LawActs/File/7689", "https://www.cbr.ru/Crosscut/LawActs/File/7691", "https://www.cbr.ru/Crosscut/LawActs/File/7694",
#         "https://www.cbr.ru/Crosscut/LawActs/File/7695", "https://www.cbr.ru/Queries/UniDbQuery/File/90134/3997"]
#
# for url in urls:
#     doc = DocumentHolder(url)
#     encoder = Encoder(doc.text)
#     encoder.encode_document()
#     print(encoder.encoded_text_by_pages)
#
#
#
