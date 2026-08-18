# 📚 PDF RAG Chatbot

An AI-powered chatbot that answers questions from uploaded PDF documents using Retrieval-Augmented Generation (RAG).

## Features

- Upload PDF files
- Extract text automatically
- Store document chunks in ChromaDB
- Semantic search
- Gemini-powered answers
- Chat history
- Source tracking

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Google Gemini
- PyPDF

## Project Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
ChromaDB
    ↓
Semantic Search
    ↓
Gemini 3.6 Flash
    ↓
Answer Generation
```

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd 06-Multi-PDF-RAG-Chatbot
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Requirements

```text
streamlit
chromadb
google-genai
pypdf
```

## Configure Gemini API Key

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

## Run

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Example Questions

```text
What is Python?
Summarize this document.
What skills does the candidate have?
What projects are mentioned?
```

## Learning Outcomes

- Gemini API Integration
- Vector Databases
- Embeddings
- ChromaDB
- Retrieval-Augmented Generation (RAG)
- Streamlit Applications
- PDF Processing
- Semantic Search

## Author

Muhammad Midlaj
B.Tech Electronics and Communication Engineering
