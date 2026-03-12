from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


def create_vector_store(documents, persist_directory="db/chroma"):
    embeddings = OllamaEmbeddings(model="llama3")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore