# 🚀 LangChain Components Overview

LangChain pipelines usually consist of **four main stages**:

  Stage          Purpose
  -------------- -----------------------------------------
  📥 **Load**    Ingest data from different sources
  ✂️ **Split**   Break large text into manageable chunks
  🧠 **Embed**   Convert text into numerical vectors
  🗄️ **Store**   Store embeddings in a vector database

------------------------------------------------------------------------

# 🧩 LangChain Pipeline Diagram

``` mermaid
flowchart LR
    A[Data Sources] --> B[Document Loaders]
    B --> C[Text Splitters]
    C --> D[Embeddings]
    D --> E[Vector Database]
    E --> F[Retriever]
    F --> G[LLM]
    G --> H[Answer / Response]
```

This represents the **complete LangChain data flow** used in most AI
systems.

------------------------------------------------------------------------

# 📥 1. Load --- Data Ingestion

Load data from different sources using:

`langchain_community.document_loaders`

📚 Documentation\
https://docs.langchain.com/oss/python/integrations/document_loaders

### Supported Document Loaders

-   📄 **TextLoader**
-   📑 **PyPDFLoader**
-   🌐 **WebBaseLoader**
-   📚 **ArxivLoader**
-   📖 **WikipediaLoader**

Example notebook:

`3.2-DataIngestion.ipynb`

### 📦 Required Python Libraries (requirements.txt)

    langchain-community
    pypdf
    bs4
    arxiv
    PyMuPDF
    wikipedia

------------------------------------------------------------------------

# ✂️ 2. Split --- Text Chunking

Large documents are split into **smaller chunks** so LLMs can process
them efficiently.

Key parameters:

-   chunk_size
-   chunk_overlap

Splitters available in:

`langchain_text_splitters`

### Common Text Splitters

  -----------------------------------------------------------------------
  Splitter                            Description
  ----------------------------------- -----------------------------------
  RecursiveCharacterTextSplitter      Splits text using chunk size or
                                      double newline

  CharacterTextSplitter               Basic character-based splitting

  HTMLHeaderTextSplitter              Splits text based on HTML headers

  RecursiveJsonSplitter               Used for JSON structured data
  -----------------------------------------------------------------------

### 📦 Required Python Libraries

    langchain-text-splitters

------------------------------------------------------------------------

# 🧠 3. Embed --- Convert Text to Vectors

Embeddings convert text into **numerical vectors** so machines
understand semantic similarity.

## 🤖 OpenAI Embeddings

``` python
from langchain_openai import OpenAIEmbeddings
```

⚠️ Paid service

API Keys\
https://platform.openai.com/settings/organization/api-keys

Common Models

-   text-embedding-3-large
-   text-embedding-3-small
-   text-embedding-ada-002

------------------------------------------------------------------------

## 🦙 Ollama Embeddings

``` python
from langchain_community.embeddings import OllamaEmbeddings
```

Download

https://ollama.com/download/windows

Install models

    ollama run llama2
    ollama run gemma:2b

------------------------------------------------------------------------

## 🤗 HuggingFace Embeddings

``` python
from langchain_huggingface import HuggingFaceEmbeddings
```

Create token

https://huggingface.co/settings/tokens

Example model

`all-MiniLM-L6-v2`

### 📦 Required Python Libraries

    langchain-openai
    sentence-transformers
    langchain_huggingface

------------------------------------------------------------------------

# 🗄️ 4. Store --- Vector Database

Embeddings are stored in **Vector Databases** for efficient retrieval.

Vector stores available in

`langchain_community.vectorstores`

### Supported Vector Databases

  Vector DB   Import
  ----------- ----------------------------------------------------
  FAISS       from langchain_community.vectorstores import FAISS
  Chroma      from langchain_chroma import Chroma

### Common Retrieval Functions

``` python
.similarity_search()

.similarity_search_with_score()

.similarity_search_by_vector()
```

### 📦 Required Python Libraries

    faiss-cpu
    chromadb
    langchain_chroma

------------------------------------------------------------------------

# 📊 Table of Important Libraries

  Library                    Purpose
  -------------------------- ------------------------
  langchain-community        Document loaders
  langchain-text-splitters   Text chunking
  langchain-openai           OpenAI embeddings
  langchain_huggingface      HuggingFace embeddings
  sentence-transformers      Embedding models
  chromadb                   Vector database
  faiss-cpu                  Similarity search
  pypdf                      PDF reading
  bs4                        Web scraping
  arxiv                      Research loader
  wikipedia                  Wikipedia loader

------------------------------------------------------------------------

# 🔎 RAG Architecture Flow

``` mermaid
flowchart LR
    A[User Question] --> B[Retriever]
    B --> C[Vector Database]
    C --> D[Relevant Documents]
    D --> E[Prompt Augmentation]
    E --> F[Large Language Model]
    F --> G[Generated Answer]
```

### RAG Process

1.  Retrieve relevant context from Vector DB
2.  Combine context with user query
3.  Send both to LLM
4.  Generate grounded answer

------------------------------------------------------------------------

# 🔁 Complete Workflow

    Load Data → Split Text → Generate Embeddings → Store in Vector DB → Retrieve → LLM → Response

------------------------------------------------------------------------

# 💡 Common Applications

-   Semantic Search
-   AI Chatbots
-   Retrieval Augmented Generation (RAG)
-   Question Answering Systems
