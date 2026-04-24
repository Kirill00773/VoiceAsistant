"""
Скрипт для инициализации векторной базы данных
"""
from rag.loader import load_txt_documents
from rag.splitter import split_documents
from rag.vector_store import create_vector_store

DATA_PATH = "data/knowledge_base"


def main():
    print("Инициализация векторной базы данных...")

    # Загрузка документов
    documents = load_txt_documents(DATA_PATH)
    print(f"[OK] Загружено документов: {len(documents)}")

    # Разбиение на чанки
    chunks = split_documents(documents)
    print(f"[OK] Создано чанков: {len(chunks)}")

    # Создание векторной базы
    create_vector_store(chunks)
    print("[OK] Векторная база создана успешно!")


if __name__ == "__main__":
    main()
