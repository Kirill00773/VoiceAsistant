from rag.loader import load_txt_documents
from rag.splitter import split_documents
from rag.vector_store import create_vector_store
from rag.qa import retrieve_context, generate_answer

DATA_PATH = "data/knowledge_base"


def main():
    # --- 1. Подготовка базы (из 3 лабы) ---
    documents = load_txt_documents(DATA_PATH)
    print(f"Загружено документов: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Создано чанков: {len(chunks)}")

    create_vector_store(chunks)
    print("Векторная база обновлена.")

    # --- 2. Ввод вопроса ---
    query = input("\nВведите вопрос: ")

    # --- 3. Поиск релевантных данных ---
    context, results = retrieve_context(query)

    print("\n=== Найденный контекст ===")
    for i, doc in enumerate(results, start=1):
        print(f"\nФрагмент {i}:")
        print(doc.page_content)

    # --- 4. Генерация ответа ---
    answer = generate_answer(query, context)

    print("\n=== Ответ ассистента ===")
    print(answer)


if __name__ == "__main__":
    main()