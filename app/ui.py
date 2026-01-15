import streamlit as st
from pypdf import PdfReader

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot (PDF)")
st.write("Upload a PDF and preview extracted text.")

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    reader = PdfReader(uploaded)

    max_pages = st.slider(
        "Max pages to extract",
        1,
        len(reader.pages),
        min(5, len(reader.pages))
    )

    text = ""
    for page in reader.pages[:max_pages]:
        text += (page.extract_text() or "") + "\n"

    st.success(f"✅ Extracted {len(text)} characters")
    st.text_area("Preview (first 3000 chars)", text[:3000], height=300)

    st.download_button(
        "⬇️ Download text (.txt)",
        text,
        file_name="extracted_text.txt"
    )

