from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import requests


DB_PATH = "db/chroma"
MODEL_NAME = "llama3"


def get_vectorstore():
    embeddings = OllamaEmbeddings(model=MODEL_NAME)

    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore


def retrieve_context(query: str, k: int = 3):
    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search_with_score(query, k=k)

    filtered_docs = []

    for doc, score in results:
        # чем меньше score — тем лучше (в Chroma)
        if score < 0.5:  # можно подбирать (0.3–0.7)
            filtered_docs.append(doc)

    if not filtered_docs:
        filtered_docs = [results[0][0]]  # fallback

    context = "\n\n".join([doc.page_content for doc in filtered_docs])

    return context, filtered_docs


def generate_answer(query: str, context: str):
    prompt = f"""
Ты — ассистент лаборатории.

Отвечай КРАТКО и ТОЛЬКО по вопросу.

Правила:
- Используй только релевантную информацию из контекста
- НЕ пересказывай весь текст
- НЕ добавляй лишние детали
- Если информации мало — ответь кратко и добавь немного от себя

Контекст:
{context}

Вопрос:
{query}

Краткий ответ:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]