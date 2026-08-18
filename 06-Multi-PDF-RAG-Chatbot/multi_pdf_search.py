import chromadb

chroma = chromadb.PersistentClient(
    path="C:/ai/multi_pdf_db"
)

collection = chroma.get_or_create_collection(
    name="documents"
)

question = input("Ask: ")

results = collection.query(
    query_texts=[question],
    n_results=3
)

for doc, meta in zip(
    results["documents"][0],
    results["metadatas"][0]
):

    print("\nSource:", meta["source"])
    print(doc)