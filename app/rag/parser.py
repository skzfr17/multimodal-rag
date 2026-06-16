from langchain_core.documents import Document
from app.config import LLAMA_API_KEY
import os
import fitz
import uuid


def parse_pdf(file_path):
    pdf = fitz.open(file_path)

    documents = []
    doc_id = str(uuid.uuid4())
    filename = os.path.basename(file_path)

    for page_num in range(len(pdf)):
        page = pdf[page_num]
        text = page.get_text("text").strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "doc_id": doc_id,
                    "file_path": file_path,
                    "filename": filename,
                    "page": page_num + 1
                }
            )
        )
    pdf.close()

    return documents