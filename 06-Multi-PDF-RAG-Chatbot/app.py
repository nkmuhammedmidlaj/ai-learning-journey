import streamlit as st
import chromadb
from google import genai

# Gemini Client
client = genai.Client()

# ChromaDB
chroma = chromadb.PersistentClient(
    path="C:/ai/multi_pdf_db"
)

collection = chroma.get_or_create_collection(
    name="documents"
)

# Title
st.title("📚 Multi-PDF AI Chatbot")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
question = st.chat_input("Ask a question")

if question:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    # Search ChromaDB
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    # Retrieved documents
    context = "\n".join(
        results["documents"][0]
    )

    # Get source PDFs
    sources = []

    for meta in results["metadatas"][0]:
        if meta and "source" in meta:
            sources.append(meta["source"])

    sources = list(set(sources))

    # Prompt
    prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the context.

If the answer is not found in the context,
say:
"I could not find that information in the documents."
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        answer = response.text

    except Exception as e:

        answer = f"Gemini Error: {e}"

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # Display answer
    with st.chat_message("assistant"):
        st.write(answer)

        if sources:
            st.write("📄 Sources:")
            for source in sources:
                st.write(f"- {source}")

    # Optional debug section
    with st.expander("Retrieved Context"):
        st.write(context)