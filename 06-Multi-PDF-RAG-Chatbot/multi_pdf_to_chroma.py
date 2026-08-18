import os
import chromadb
from pypdf import PdfReader

chroma = chromadb.PersistentClient(
    path="C:/ai/multi_pdf_db"
)

collection = chroma.get_or_create_collection(
    name="documents"
)

pdf_folder = "C:/ai/pdfs"

doc_id = 0

for filename in os.listdir(pdf_folder):

    if filename.endswith(".pdf"):

        filepath = os.path.join(pdf_folder, filename)

        reader = PdfReader(filepath)

        text = ""

        for page in reader.pages:
            text += page.extract_text()

        chunks = [
            c.strip()
            for c in text.split("\n")
            if c.strip()
        ]

        for chunk in chunks:

            collection.upsert(
                ids=[str(doc_id)],
                documents=[chunk],
                metadatas=[{
                    "source": filename
                }]
            )

            doc_id += 1

print("Finished!")