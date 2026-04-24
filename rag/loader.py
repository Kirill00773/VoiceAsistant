from pathlib import Path
from langchain_core.documents import Document

def clean_text(text: str) -> str:
    # Убираем только лишние пробелы в строках,
    # но сохраняем структуру строк и абзацев
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()

def load_txt_documents(folder: str):
    documents = []
    path = Path(folder)

    for file_path in path.glob("*.txt"):
        # Читаем как есть, сохраняя структуру
        text = file_path.read_text(encoding="utf-8")
        text = clean_text(text)

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name}
            )
        )
    return documents