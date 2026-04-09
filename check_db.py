from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def main():
    embeddings = OllamaEmbeddings(model="llama3")

    vectorstore = Chroma(
        persist_directory="db/chroma",
        embedding_function=embeddings
    )

    data = vectorstore.get()

    print("Количество записей:", len(data["ids"]))

    for i in range(len(data["ids"])):
        print(f"\n--- Запись {i + 1} ---")
        print("ID:", data["ids"][i])
        print("Текст:", data["documents"][i])
        print("Метаданные:", data["metadatas"][i])


if __name__ == "__main__":
    main()