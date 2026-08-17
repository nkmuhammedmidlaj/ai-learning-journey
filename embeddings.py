from google import genai
import math

client = genai.Client()

texts = [
    "How do I learn Python?",
    "What is the best way to study Python?",
    "How can I repair my car?"
]


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))

    return dot_product / (magnitude_a * magnitude_b)


vectors = [get_embedding(text) for text in texts]

similarity_python = cosine_similarity(vectors[0], vectors[1])
similarity_car = cosine_similarity(vectors[0], vectors[2])

print("Python vs Python similarity:", similarity_python)
print("Python vs Car similarity:", similarity_car)