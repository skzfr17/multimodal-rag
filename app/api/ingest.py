from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from app.rag.parser import parse_pdf
from app.rag.embedder import chunk_documents, create_vectorstore

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    os.makedirs("data/uploads", exist_ok=True)
    file_path = f"data/uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse PDF
    docs = parse_pdf(file_path)

    if not docs:
        raise HTTPException(
            status_code=400,
            detail="Dokumen gagal diparse atau kosong."
        )
    
    doc_id = docs[0].metadata.get("doc_id")

    # Chunking
    chunks = chunk_documents(docs)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="Chunking gagal."
        )

    # Save to vector DB
    vectordb = create_vectorstore(chunks)

    return{
        "message": "Ingestion success",
        "doc_id": doc_id,
        "filename": file.filename,
        "documents": len(docs),
        "chunks": len(chunks)
    }