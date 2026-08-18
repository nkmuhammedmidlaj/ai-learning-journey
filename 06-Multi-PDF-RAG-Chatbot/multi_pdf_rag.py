import chromadb
from google import genai

# Gemini client
client = genai.Client()

# ChromaDB
chroma = chromadb.PersistentClient(
    path="C:/ai/multi_pdf_db"
)

collection = chroma.get_or_create_collection(
    name="documents"
)

# Ask user
question = input("Ask: ")

# Search ChromaDB
results = collection.query(
    query_texts=[question],
    n_results=3
)

# Get retrieved chunks
context = "\n".join(results["documents"][0])

# Create prompt
prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the context.
"""

# Gemini response
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nAnswer:")
print(response.text)