import streamlit as st
import requests
import os
import base64
import time

# =========================
# API ENDPOINT
# =========================
INGEST_URL = "http://127.0.0.1:8000/ingest"
QUERY_URL = "http://127.0.0.1:8000/query"

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Multimodal RAG System",
    layout="wide"
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# SESSION STATE
# =========================
st.session_state.setdefault("pdf_path", None)
st.session_state.setdefault("selected_page", None)
st.session_state.setdefault("ingested", False)
st.session_state.setdefault("answer", None)
st.session_state.setdefault("sources", [])

# =========================
# PDF VIEWER
# =========================
def show_pdf(pdf_path, page=None):

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    cache_buster = int(time.time())

    page_param = f"#page={page}" if page else ""

    pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}{page_param}&v={cache_buster}"
            width="100%"
            height="800">
        </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("Multimodal RAG System")
st.caption("Upload >> Ingest >> Ask >> Open Source Page")

left, right = st.columns([1.1, 1], gap="large")

# ======================================================
# LEFT COLUMN
# ======================================================
with left:

    # ================= UPLOAD =================
    st.header("Upload Document")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        save_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.pdf_path = save_path
        st.success("PDF loaded successfully!")

        if st.button("Ingest Document"):

            with st.spinner("Processing document..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf"
                    )
                }

                res = requests.post(INGEST_URL, files=files)

                if res.status_code == 200:

                    st.session_state.ingested = True
                    result = res.json()

                    st.success("Ingestion completed!")

                    c1, c2 = st.columns(2)
                    c1.metric("Documents", result["documents"])
                    c2.metric("Chunks", result["chunks"])

                else:
                    st.error("Ingestion failed!")

    st.divider()

    # ================= ASK QUESTION =================
    st.header("Ask Question")

    if not st.session_state.ingested:
        st.info("Upload and ingest document first.")
    else:

        question = st.text_input("Enter your question")

        if st.button("Ask"):

            if question:

                st.session_state.selected_page = None

                with st.spinner("Thinking..."):

                    res = requests.post(
                        QUERY_URL,
                        json={"question": question}
                    )

                    data = res.json()

                    st.session_state.answer = data["answer"]
                    st.session_state.sources = data.get("sources", [])

            else:
                st.warning("Please enter a question.")

        # ================= ANSWER =================
        if st.session_state.answer:

            st.subheader("Answer")
            st.success(st.session_state.answer)

            st.subheader("Source Pages")

            if st.session_state.sources:

                pages = sorted(set(
                    s.get("page")
                    for s in st.session_state.sources
                    if s.get("page") is not None
                ))

                for page in pages:

                    if st.button(
                        f"Open Page {page}",
                        key=f"open_page_{page}"
                    ):
                        st.session_state.selected_page = page

            else:
                st.info("No source pages found.")

# ======================================================
# RIGHT COLUMN — PDF VIEWER
# ======================================================
with right:

    st.header("Source Viewer")

    if (
        st.session_state.pdf_path
        and st.session_state.selected_page is not None
    ):

        st.info(
            f"Showing Page {st.session_state.selected_page}"
        )

        show_pdf(
            st.session_state.pdf_path,
            st.session_state.selected_page
        )

    else:
        st.info("Click **Open Page** to preview PDF page.")