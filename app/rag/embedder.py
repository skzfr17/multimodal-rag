from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "data/vectordb"

class E5Embedding(HuggingFaceEmbeddings):

    def embed_documents(self, texts):
        texts = [f"passage: {t}" for t in texts]
        return super().embed_documents(texts)
    
    def embed_query(self, text):
        return super().embed_query(f"query: {text.strip()}")
    
# =====================
# EMBEDDING (SINGLE SOURCE)
# =====================
def get_embedding():
    return E5Embedding(
        model_name="intfloat/multilingual-e5-base",
        encode_kwargs={"normalize_embeddings": True}
    )


# =====================
# CHUNKING
# =====================
def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=[
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    all_chunks = []

    for doc in documents:
        chunks = splitter.split_documents([doc])

        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "doc_id": doc.metadata.get("doc_id"),
                "source": doc.metadata.get("source"),
                "file_path": doc.metadata.get("file_path"),
                "page": doc.metadata.get("page"),
                "chunk_id": f"p{doc.metadata.get('page')}_{i}"
            })

            all_chunks.append(chunk)

    return all_chunks


# =====================
# CREATE VECTOR DB
# =====================
def create_vectorstore(chunks):

    embedding = get_embedding()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=PERSIST_DIR
    )

    vectordb.persist()

    return vectordb


# =====================
# LOAD VECTOR DB
# =====================
def load_vectorstore():

    embedding = get_embedding()

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding
    )

    return vectordb