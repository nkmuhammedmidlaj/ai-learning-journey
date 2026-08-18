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

st.title("📚 PDF RAG Chatbot")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# PDF Upload
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    chunks = []
    chunk_size = 800

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

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

    st.success(
        f"{uploaded_file.name} uploaded successfully!"
    )

# Chat Input
question = st.chat_input(
    "Ask a question about your PDFs"
)

if question:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    # Search ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=10
    )

    context = "\n".join(
        results["documents"][0]
    )

    # Sources
    sources = []

    if results["metadatas"]:
        for meta in results["metadatas"][0]:
            if meta and "source" in meta:
                sources.append(meta["source"])

    sources = list(set(sources))

    prompt = f"""
You are a helpful assistant.

Use ONLY the information in the context.

Context:
{context}

Question:
{question}

If the answer is not available in the context,
say:
"I could not find that information in the uploaded documents."
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        answer = response.text

    except Exception as e:

        answer = f"Gemini Error: {e}"

    # Save Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display Answer
    with st.chat_message("assistant"):
        st.write(answer)

        if sources:
            st.write("📄 Sources:")
            for source in sources:
                st.write(f"- {source}")

    # Debug Context
    with st.expander("Retrieved Context"):
        st.write(context)