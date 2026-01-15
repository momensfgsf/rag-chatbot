from pypdf import PdfReader

def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        full_text.append(text)
    return "\n".join(full_text)

if __name__ == "__main__":
    text = extract_text("data/sample.pdf")
    print("✅ Extracted characters:", len(text))
    print("\n--- Preview (first 800 chars) ---\n")
    print(text[:800])
