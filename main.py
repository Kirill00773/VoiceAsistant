from rag.loader import load_txt_documents
from rag.splitter import split_documents
from rag.vector_store import create_vector_store


DATA_PATH = "data/knowledge_base"


def main():
    documents = load_txt_documents(DATA_PATH)
    print(f"Загружено документов: {len(documents)}")

    chunks = split_documents(documents)
    print(f"Создано чанков: {len(chunks)}")

    create_vector_store(chunks)
    print("Векторная база успешно создана.")


if __name__ == "__main__":
    main()