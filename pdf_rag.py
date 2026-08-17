import chromadb
from google import genai

client = genai.Client()

chroma = chromadb.PersistentClient(
    path="C:/ai/pdf_db"
)

collection = chroma.get_or_create_collection(
    name="pdf_notes"
)

question = input("Ask: ")

results = collection.query(
    query_texts=[question],
    n_results=2
)

context = "\n".join(results["documents"][0])

prompt = f"""
Context:
{context}

Question:
{question}

Answer only using the context.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nAnswer:")
print(response.text)