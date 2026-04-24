from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    # Увеличиваем размер до 1200, чтобы смысловые блоки (типа FAQ)
    # гарантированно влезали в один чанк целиком.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        # Разрезаем сначала по двойному переносу (абзацам)
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)