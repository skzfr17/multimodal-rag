from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embedder import load_vectorstore
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

router = APIRouter()


# =========================
# Request Schema
# =========================
class QueryRequest(BaseModel):
    question: str


# =========================
# LOAD VECTORSTORE
# =========================
vectorstore = load_vectorstore()


# =========================
# LLM (MODEL JAWABAN)
# =========================
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)


# =========================
# QUERY ENDPOINT
# =========================
@router.post("/query")
async def query(req: QueryRequest):

    question = f"query: {req.question.strip()}"

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3
        }
    )

    docs = retriever.invoke(question)

    if not docs:
        return {
            "answer": "Informasi tidak ditemukan dalam dokumen.",
            "sources": []
        }

    context = []
    sources = []

    for d in docs:
        page = d.metadata.get("page")
        doc_id = d.metadata.get("doc_id")
        file_path = d.metadata.get("file_path")
        source_name = d.metadata.get("source")

        context.append(
            f"[Halaman {page}]\n{d.page_content}"
        )

        sources.append({

            "page": page,
            "doc_id": doc_id,
            "file_path": file_path,
            "source": source_name
        }
        )

    full_context = "\n\n".join(context)

    prompt = f"""
Kamu adalah analis dokumen Laporan Keuangan Bank Mandiri.

Gunakan informasi dari KONTEKS berikut.

ATURAN:
- Jawab berdasarkan teks yang PALING relevan.
- Boleh merangkum kalimat dari konteks.
- Jangan menambahkan pengetahuan luar dokumen.
- WAJIB menyebutkan nomor halaman dari konteks.
- Jika informasi benar-benar tidak ada, baru katakan:
  "Informasi tidak ditemukan dalam dokumen."

FORMAT JAWABAN:

Jawaban:
...

Halaman:
{page}

KONTEKS:
{context}

PERTANYAAN:
{req.question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip(),
        "sources": sources
    }