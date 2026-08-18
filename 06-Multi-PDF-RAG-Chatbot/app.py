import streamlit as st
import chromadb
from pypdf import PdfReader
from google import genai

# Gemini
client = genai.Client()

# ChromaDB
chroma = chromadb.PersistentClient(
    path="C:/ai/upload_db"
)

collection = chroma.get_or_create_collection(
    name="pdfs"
)

st.title("📚 Upload & Chat PDF")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success("PDF loaded successfully!")

    # Chunking
    chunks = []
    chunk_size = 800

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    # Store in ChromaDB
    for i, chunk in enumerate(chunks):

        try:
            collection.add(
                documents=[chunk],
                ids=[f"{uploaded_file.name}_{i}"],
                metadatas=[
                    {"source": uploaded_file.name}
                ]
            )

        except:
            pass

    st.success(f"Stored {len(chunks)} chunks!")

# Ask Question
question = st.text_input(
    "Ask a question about uploaded PDFs"
)

if question:

    results = collection.query(
        query_texts=[question],
        n_results=10
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are a helpful assistant.

Use ONLY the information provided in the context.

Context:
{context}

Question:
{question}

If the answer is not found in the context,
say:
"I could not find that information in the uploaded documents."
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        st.subheader("Answer")
        st.write(response.text)

        with st.expander("Retrieved Context"):
            st.write(context)

    except Exception as e:

        st.error(f"Gemini Error: {e}")
