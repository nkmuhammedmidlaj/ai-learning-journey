from google import genai
import math

client = genai.Client()

# Read knowledge base
with open(r"C:\ai\knowledge.txt", "r") as file:
    text = file.read()

# Split into chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))

    return dot / (magnitude_a * magnitude_b)


# Create embeddings for document chunks
chunk_vectors = [
    get_embedding(chunk)
    for chunk in chunks
]

# Ask a question
question = input("Ask: ")

# Embed the question
question_vector = get_embedding(question)

# Calculate similarity
scores = [
    cosine_similarity(question_vector, vector)
    for vector in chunk_vectors
]

# Get top 3 chunks
top_k = 3

top_indices = sorted(
    range(len(scores)),
    key=lambda i: scores[i],
    reverse=True
)[:top_k]

# Display retrieved information
print("\nRetrieved information:")

for i in top_indices:
    print("\n---")
    print("Similarity:", scores[i])
    print(chunks[i])