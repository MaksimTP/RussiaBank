import subprocess
import os
from pdfreader import PDFDocument, SimplePDFViewer
from sentence_transformers import SentenceTransformer
import numpy as np


class DocumentHolder:

    try:
        os.mkdir("docs")
    except:
        pass

    N = len(os.listdir("docs"))

    def __init__(self, url) -> None:
        self.url = url
        self.text = {}
        self.load_doc()
        self.read_file()

    def load_doc(self):
        try:
            subprocess.call(
                f"curl -o docs/{self.N}.pdf {self.url}",
                shell=True,
                executable="/bin/bash",
            )
            self.filename = f"{self.N}.pdf"
            self.N += 1
        except Exception as ex:
            print(ex)

    def read_file(self):
        self.fd = open("docs/" + self.filename, "rb")
        self.viewer = SimplePDFViewer(self.fd)

        cnt = 1
        for canvas in self.viewer:
            self.text[cnt] = "".join(canvas.strings)
            cnt += 1


# doc = DocumentHolder("https://www.cbr.ru/Crosscut/LawActs/File/7690")


def get_detailed_instruct(
    query: str,
    task_description: str = "Given a web search query, retrieve relevant passages that answer the query",
) -> str:
    return f"Instruct: {task_description}\nQuery: {query}"


class Encoder:
    def __init__(
        self,
        text_by_pages: dict[int, str],
        document_name: str = "",
        chunk_size: int = 1,
    ) -> None:
        self.text_by_pages = text_by_pages
        self.document_name = document_name
        self.chunk_size = chunk_size
        self.encoded_text_by_pages = text_by_pages.copy()
        self.model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

    def encode_document(self):
        for page_key in self.text_by_pages:
            chunk = ""
            for i in range(self.chunk_size):
                chunk += self.text_by_pages.get(page_key + i, "")
            embedding = self.model.encode(chunk, normalize_embeddings=True)
            self.encoded_text_by_pages[page_key] = embedding
        return self.encoded_text_by_pages

    def encode_query(self, query: str):
        return self.model.encode(get_detailed_instruct(query))


class VectorCalculator:
    def __init__(
        self, encoded_query, encoded_document_by_chunks: dict[int, str]
    ) -> None:
        self.encoded_query = encoded_query
        self.encoded_document_by_chunks = encoded_document_by_chunks
        self.scores = []

    def get_score_by_chunk(self, chunk_num):
        vec = self.encoded_document_by_chunks[chunk_num]
        return vec @ self.encoded_query / np.linalg.norm(vec)

    def get_scores(self):
        self.scores = [
            self.get_score_by_chunk(chunk_num)
            for chunk_num in self.encoded_document_by_chunks
        ]
        return self.scores


class RAG:
    pass
