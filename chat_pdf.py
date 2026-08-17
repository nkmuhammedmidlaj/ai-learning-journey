import chromadb
from google import genai

client = genai.Client()

chroma = chromadb.PersistentClient(
    path="C:/ai/pdf_db"
)

collection = chroma.get_or_create_collection(
    name="pdf_notes"
)

history = []

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    results = collection.query(
        query_texts=[question],
        n_results=2
    )

    context = "\n".join(
        results["documents"][0]
    )

    conversation = "\n".join(history)

    prompt = f"""
Context:
{context}

Conversation:
{conversation}

Question:
{question}

Answer using the context and conversation.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    answer = response.text

    print("\nAI:", answer)

    history.append(f"User: {question}")
    history.append(f"AI: {answer}")