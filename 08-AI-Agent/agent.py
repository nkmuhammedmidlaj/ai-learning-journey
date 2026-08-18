import chromadb
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

print("🤖 AI Agent Started")
print("Type 'exit' to quit\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    try:

        # Retrieve relevant chunks
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        context = "\n".join(
            results["documents"][0]
        )

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the information in the context.

Context:
{context}

Question:
{question}

If the answer is not found in the context,
say:
"I could not find that information in the documents."
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print("\nAgent:", response.text)
        print()

    except Exception as e:

        print("\nError:", e)
        print()