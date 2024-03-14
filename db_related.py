from documents import *
from utils import *
from sentence_transformers import SentenceTransformer
import clickhouse_connect


def set_to_db(client, data):
    """
    Функция set_to_db добавляет записи в таблицу test_table.

    Параметры:
    - client: клиент для работы с базой данных
    - data: данные для добавления

    Возвращаемое значение:
    Нет возвращаемого значения.
    """
    client.insert(
        "test_table",
        data,
        column_names=[
            "id",
            "document_name",
            "document_url",
            "create_date",
            "modification_date",
            "chunk_number",
            "chunk_embeding",
            "chunk_text",
        ],
    )


def load_docs_into_db(
    vmodel=SentenceTransformer("intfloat/multilingual-e5-large-instruct"),
    client=clickhouse_connect.get_client(
        host="localhost", port=8123, username="default", password=""
    ),
    path_to_docs_folder="docs_new",
):
    """
    Метод для загрузки документов в базу данных.

    Параметры:
    - vmodel: модель для векторизации текста
    - client: экземпляр клиента для работы с базой данных
    - path_to_docs_folder: str, путь к папке с документами

    Возвращаемое значение:
    - None

    Пример использования:
    load_docs_into_db(model, db_client, "path/to/docs/folder")
    """
    reader = Reader()
    id = 1

    for filename in os.listdir(path_to_docs_folder):
        try:
            text = reader.read_file(filename)
            file_url = get_link(filename)
            metadata = get_metadata(filename)
            create_date = metadata[0]
            modification_date = metadata[1]
            if text != "":
                encoder = Encoder(text, vmodel)
                encoder.encode_document()
                for key, value in encoder.encoded_text_by_chunks.items():
                    chunk_text = encoder.dict_by_chunks[key]
                    print(
                        [
                            [
                                id,
                                filename,
                                file_url,
                                create_date,
                                modification_date,
                                key,
                                value,
                                chunk_text,
                            ]
                        ]
                    )
                    client.insert(
                        "test_table",
                        [
                            [
                                id,
                                filename,
                                file_url,
                                create_date,
                                modification_date,
                                key,
                                value,
                                chunk_text,
                            ]
                        ],
                        column_names=[
                            "id",
                            "document_name",
                            "document_url",
                            "create_date",
                            "modification_date",
                            "chunk_number",
                            "chunk_embeding",
                            "chunk_text",
                        ],
                    )
            id += 1
        except Exception as ex:
            print(ex)
