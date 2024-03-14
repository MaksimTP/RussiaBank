import spacy
import numpy as np

nlp = spacy.load("ru_core_news_lg")

def process(text: str) -> tuple[list[str], np.ndarray]:
    """
    Функция process выполняет обработку текста, включая разбиение на предложения, вычисление векторов предложений и их нормализацию.

    Параметры:
    - text: str, входной текст для обработки

    Возвращаемые значения:
    - sents: List[str], список предложений
    - vecs: np.ndarray, массив векторов предложений

    Пример использования:
    sents, vecs = process("Ваш текст для обработки")
    """
    doc = nlp(text)
    sents = list(doc.sents)
    vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])
    print(len(sents))
    return sents, vecs


def cluster_text(
    sents: list[str], vecs: np.ndarray, threshold: float
) -> list[list[int]]:
    """
    Функция cluster_text выполняет кластеризацию предложений на основе векторов и заданного порога.

    Параметры:
    - sents: List[str], список предложений
    - vecs: np.ndarray, массив векторов предложений
    - threshold: float, порог для кластеризации

    Возвращаемое значение:
    - clusters: List[List[int]], список кластеров предложений

    Пример использования:
    clusters = cluster_text(sents, vecs, 0.7)
    """
    clusters = [[0]]
    for i in range(1, len(sents)):
        if np.dot(vecs[i], vecs[i - 1]) < threshold:
            clusters.append([])
        clusters[-1].append(i)

    return clusters


def clean_text(input_text: str) -> str:
    return input_text.lower()


def get_chunks_dict(text: str) -> dict[int, str]:
    """
    Функция get_chunks_dict разбивает входной текст на кластеры предложений на основе векторов и заданного порога.
    Возвращает словарь, в котором ключи - номера кластеров, а значения - тексты предложений в кластерах.

    Параметры:
    - text: str, входной текст для обработки

    Возвращаемое значение:
    - Dict[int, str], словарь с номерами кластеров и текстами предложений в каждом кластере

    Пример использования:
    chunks_dict = get_chunks_dict("Ваш текст для разбиения на кластеры")
    """
    clusters_lens = []
    final_texts = []

    threshold = 0.3  # Порог для кластаризации меньших текста
    sents, vecs = process(text)

    clusters = cluster_text(sents, vecs, threshold)

    for cluster in clusters:
        cluster_txt = clean_text(" ".join([sents[i].text for i in cluster]))
        cluster_len = len(cluster_txt)

        if cluster_len < 350:  # Минимальный размер чанка в количестве символов
            continue

        elif cluster_len > 3500:  # Максимальный размер чанка в количестве символов
            threshold = (
                0.6  # Обновление порога для кластеризации более крупных частей текста
            )
            sents_div, vecs_div = process(cluster_txt)
            reclusters = cluster_text(sents_div, vecs_div, threshold)

            for subcluster in reclusters:
                div_txt = clean_text(" ".join([sents_div[i].text for i in subcluster]))
                div_len = len(div_txt)

                if div_len < 350 or div_len > 3500:  # Проверка размеров подкластера
                    continue

                clusters_lens.append(div_len)
                final_texts.append(div_txt)

        else:
            clusters_lens.append(cluster_len)
            final_texts.append(cluster_txt)

    chunks = {}
    for i in range(0, len(clusters_lens)):
        chunks[i + 1] = final_texts[i]

    return chunks
