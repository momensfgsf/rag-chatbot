import streamlit as st
from pypdf import PdfReader
import re


# -----------------------------
# Helpers
# -----------------------------
def chunk_text(text, chunk_size=800):
    text = text.replace("\n", " ")
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks


def score_chunk(question, chunk):
    # simple keyword scoring (no AI libraries needed)
    q_words = re.findall(r"\w+", question.lower())
    c_lower = chunk.lower()

    score = 0
    for w in q_words:
        if len(w) > 2 and w in c_lower:
            score += 1
    return score


def search_chunks(question, chunks, top_k=3):
    scored = [(chunk, score_chunk(question, chunk)) for chunk in chunks]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [c for c, s in scored[:top_k] if s > 0]


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot (PDF)")
st.write("Upload a PDF, extract text, then ask questions to search inside it.")

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

    # Make chunks
    chunks = chunk_text(text)

    st.subheader("Ask the PDF")
    question = st.text_input("Type your question")

    if question:
        best_chunks = search_chunks(question, chunks, top_k=3)

        if best_chunks:
            st.write("✅ Top relevant parts:")
            for c in best_chunks:
                st.info(c[:600])
        else:
            st.warning("No strong matches found. Try different keywords.")





