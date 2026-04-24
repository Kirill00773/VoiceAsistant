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
Ты — умный голосовой ассистент лаборатории. Твоя задача — помогать пользователю в разговорном стиле.

Правила ответа:
1. Анализируй тему вопроса и отвечай КОНКРЕТНО по ней
2. Используй разговорный, дружелюбный стиль
3. Если в вопросе есть цифры или буквы — произноси их чётко (например: "три", "пять", "буква А")
4. Если вопрос не по теме лаборатории — вежливо скажи, что можешь помочь только с вопросами о лаборатории
5. Добавляй немного контекста от себя, чтобы ответ был полезнее
6. Отвечай кратко, но информативно (2-4 предложения)

Контекст из базы знаний:
{context}

Вопрос пользователя:
{query}

Твой ответ (разговорным стилем):
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Извини, у меня проблемы с подключением к модели. Ошибка: {str(e)}"