import streamlit as st
from pypdf import PdfReader
from rag import chunk_text, build_index, search_chunks
import google.generativeai as genai

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot (PDF)")
st.write("Upload a PDF, extract text, then ask questions to search inside it.")

# ✅ Gemini Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ GEMINI_API_KEY not found. Add it in Streamlit Secrets.")

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

    # ✅ Build semantic index
    chunks = chunk_text(text)
    model, index = build_index(chunks)

    st.subheader("Ask the PDF")
    question = st.text_input("Type your question")

    if question:
        best_chunks = search_chunks(question, chunks, model, index, top_k=3)

        st.write("✅ Top relevant parts used:")
        for c in best_chunks:
            st.info(c[:600])

        # ✅ Final AI Answer using Gemini
        if "GEMINI_API_KEY" in st.secrets:
            context = "\n\n".join(best_chunks)

            prompt = f"""
You are a helpful assistant.
Answer the user's question using ONLY the context below.
If the answer is not in the context, say: "I couldn't find that in the PDF."

CONTEXT:
{context}

QUESTION:
{question}

FINAL ANSWER:
"""

            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            response = gemini_model.generate_content(prompt)

            st.subheader("🤖 AI Answer")
            st.write(response.text)





