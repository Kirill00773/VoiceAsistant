from pathlib import Path
from langchain_core.documents import Document
import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_txt_documents(folder: str):
    documents = []

    for file_path in Path(folder).glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        text = clean_text(text)

        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name}
            )
        )

    return documents