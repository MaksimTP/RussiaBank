import subprocess
import os
from pdfreader import SimplePDFViewer
import numpy as np
from subprocess import run, STDOUT, PIPE
from preprocessing_and_chunking import *

# torch.set_num_threads(4)# если cuda, отрубаем это. Грузит проц, но ни*** не дает =( прирост менее 20%


class Reader:
    def read_file(self, filename: str) -> str:
        """
        Метод read_file читает содержимое файла и возвращает текст в зависимости от формата файлов (.doc или .pdf).

        Параметры:
        - filename: str, имя файла для чтения

        Возвращаемое значение:
        - str, текст из файла

        Пример использования:
        reader = Reader()
        text = reader.read_file("example.doc")
        """

        if filename.lower().endswith(".doc"):

            cmd = f"/bin/antiword {os.getcwd()}/docs_new/ves091230078.doc"

            file_text = run(cmd.split(), stdout=PIPE, stderr=STDOUT, text=True)

        else:

            with open(os.getcwd() + "/docs_new/" + filename, "rb") as file:

                if filename.lower().endswith(".pdf"):

                    viewer = SimplePDFViewer(file)

                    file_text = ""

                    for canvas in viewer:

                        file_text += "".join(canvas.strings)

            if file_text[:50].isascii():

                file_text = ""

        return file_text


class DocumentHolder:
    """
    Класс DocumentHolder предназначен для загрузки и хранения документов.

    Атрибуты:
    - url: str, URL-адрес для загрузки документа
    - text: str, текст из загруженного документа
    - filename: str, имя загруженного файла

    Методы:
    - __init__: конструктор класса
    - load_doc: метод для загрузки документа с помощью curl

    Пример использования:
    holder = DocumentHolder("http://example.com/document.pdf")
    """

    try:

        os.mkdir("docs_new")

    except:

        pass

    N = len(os.listdir("docs_new"))

    def __init__(self, url) -> None:
        """
        Конструктор класса DocumentHolder.

        Параметры:
        - url: str, URL-адрес для загрузки документа
        """
        self.url = url
        self.text = ""
        self.load_doc()
        self.read_file()

    def load_doc(self):
        """
        Метод для загрузки документа с помощью curl.
        """
        try:

            subprocess.call(
                f"curl -o docs_new/{self.N}.pdf {self.url}",
                shell=True,
                executable="/bin/bash",
            )

            self.filename = f"{self.N}.pdf"

            self.N += 1

        except Exception as ex:

            print(ex)

    def read_file(self):
        """
        Метод read_file отвечает за чтение содержимого файла и его обработку.

        Параметры:
        Нет входных параметров, так как метод использует атрибуты экземпляра класса.

        Возвращаемое значение:
        Нет возвращаемого значения, так как метод обрабатывает содержимое файла.

        Пример использования:
        holder = DocumentHolder("http://example.com/document.pdf")
        holder.read_file()
        """
        self.fd = open("docs_new/" + self.filename, "rb")

        self.viewer = SimplePDFViewer(self.fd)

        for canvas in self.viewer:

            self.text += "".join(canvas.strings)


class Encoder:
    def __init__(self, doc_text: str, model, chunk_size: int = 1) -> None:
        """
        Конструктор класса Encoder.

        Параметры:
        - doc_text: str, текст документа для кодирования
        - model: модель для кодирования текста
        - chunk_size: int, размер части для разделения текста (по умолчанию 1)

        Возвращаемое значение:
        Нет

        Пример использования:
        encoder = Encoder("text", model)
        """
        self.doc_text = doc_text
        self.dict_by_chunks = get_chunks_dict(self.doc_text)
        self.document_name = ""
        self.encoded_text_by_chunks = self.dict_by_chunks.copy()
        self.model = model

    def encode_document(self) -> dict[int, list[float]]:
        """
        Метод для кодирования документа.

        Параметры:
        Нет входных параметров

        Возвращаемое значение:
        - dict[int, list[float]], закодированный текст по частям

        Пример использования:
        encoded_text = encoder.encode_document()
        """
        for chunk_num in self.dict_by_chunks:

            embedding = self.model.encode(
                self.dict_by_chunks[chunk_num], normalize_embeddings=True
            )

            self.encoded_text_by_chunks[chunk_num] = embedding

        return self.encoded_text_by_chunks

    def encode_query(self, query: str) -> list[float]:
        """
        Метод для кодирования запроса.

        Параметры:
        - query: str, текст запроса

        Возвращаемое значение:
        - list[float], закодированный текст запроса

        Пример использования:
        encoded_query = encoder.encode_query("example query")
        """
        return self.model.encode(query)


class VectorCalculator:
    def __init__(
        self, encoded_query: list[float], encoded_document_by_chunks: dict[int, str]
    ) -> None:
        """
        Конструктор класса VectorCalculator.

        Параметры:
        - encoded_query: list[float], закодированный текст запроса
        - encoded_document_by_chunks: dict[int, str], закодированный текст документа по частям

        Возвращаемое значение:
        Нет

        Пример использования:
        calculator = VectorCalculator(encoded_query, encoded_document_by_chunks)
        """
        self.encoded_query = encoded_query
        self.encoded_document_by_chunks = encoded_document_by_chunks
        self.scores = []

    def get_score_by_chunk(self, chunk_num) -> float:
        """
        Метод для получения оценки по части закодированного документа.

        Параметры:
        - chunk_num: int, номер части закодированного документа

        Возвращаемое значение:
        - float, оценка по части закодированного документа

        Пример использования:
        score = calculator.get_score_by_chunk(1)
        """
        vec = self.encoded_document_by_chunks[chunk_num]

        return vec @ self.encoded_query / np.linalg.norm(vec)

    def get_scores(self) -> list[float]:
        """
        Метод для получения оценок по всем частям закодированного документа.

        Параметры:
        Нет входных параметров

        Возвращаемое значение:
        - list[float], оценки по всем частям закодированного документа

        Пример использования:
        scores = calculator.get_scores()
        """
        self.scores = [
            self.get_score_by_chunk(chunk_num)
            for chunk_num in self.encoded_document_by_chunks
        ]

        return self.scores
