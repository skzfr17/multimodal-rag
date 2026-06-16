# MULTIMODAL-RAG

## Deskripsi
MULTIMODAL-RAG adalah aplikasi berbasis Streamlit yang menerapkan konsep Retrieval-Augmented Generation (RAG) untuk menjawab pertanyaan berdasarkan dokumen yang diberikan. Aplikasi ini mendukung pemrosesan dokumen dan memanfaatkan Large Language Model (LLM) untuk menghasilkan jawaban yang relevan.

## Fitur
- Upload dokumen
- Retrieval-Augmented Generation (RAG)
- Antarmuka berbasis Streamlit
- Menjawab pertanyaan berdasarkan isi dokumen

## Teknologi
- Python
- Streamlit
- LangChain
- ChromaDB
- Groq API
- LlamaParse Cloud

## Struktur Project

```text
MULTIMODAL-RAG/
├── app/
├── data/
├── requirements.txt
├── streamlit_app.py
└── README.md
```
## Instalasi

1. Clone repository

```bash
git clone https://github.com/skzfr17/multimodal-rag.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Buat file `.env`

```env
GROQ_API_KEY=your_groq_api_key
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
```

4. Jalankan aplikasi

```bash
streamlit run streamlit_app.py
```

## Author

**Bayyinahtun Dwi Sumatri**
