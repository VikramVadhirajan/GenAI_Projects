# RAG Context Generation 🔎📚

This project demonstrates how to **generate relevant context for Retrieval-Augmented Generation (RAG) pipelines** using Large Language Models and vector search.

The goal is to prepare and retrieve **high-quality contextual information** before sending a prompt to an LLM so that the model produces **more accurate and grounded responses**.

------------------------------------------------------------------------

# 📌 Project Overview

Large Language Models (LLMs) often generate responses based only on their training data. RAG improves this by **retrieving relevant information from external knowledge sources** before generating the response.

This project focuses specifically on the **context generation stage** of the RAG pipeline.

The system retrieves relevant information and prepares it as structured context that can be injected into an LLM prompt.

------------------------------------------------------------------------

# 🧠 RAG Workflow

``` id="rag_flow"
User Query
   │
   ▼
Embedding Model
   │
   ▼
Vector Database Search
   │
   ▼
Relevant Documents Retrieved
   │
   ▼
Context Construction
   │
   ▼
LLM Prompt Generation
```

------------------------------------------------------------------------

# 🎯 Objective

The objective of this project is to:

-   Convert user queries into embeddings
-   Retrieve relevant documents from a vector database
-   Generate structured context for LLM prompts
-   Improve the accuracy of LLM responses

------------------------------------------------------------------------

# 📂 Project Structure

``` id="rag_struct"
001_RAG_Context_Generation/
│
├── experiments.ipynb
│   Notebook containing the implementation of the RAG context pipeline
│
├── requirements.txt
│
└── README.md
```

------------------------------------------------------------------------

# ⚙️ Technologies Used

Python LangChain Embedding Models Vector Databases (Chroma / FAISS) Jupyter Notebook

------------------------------------------------------------------------

## 🔄 Project Workflow

This project follows a **Retrieval-Augmented Generation (RAG) pipeline with conversational memory**. The system allows users to ask questions about a document while maintaining chat history.

### 1. Document Loading

The system starts by loading the source document (`budget_speech.pdf`).
A document loader reads the PDF and extracts the text so that it can be processed by the AI pipeline.

---

### 2. Text Splitting

Since LLMs cannot process very large documents directly, the extracted text is split into smaller chunks.

* The document is divided into manageable text segments.
* Overlapping chunks are often used to preserve context between sections.

This step ensures efficient retrieval and better contextual understanding.

---

### 3. Embedding Generation

Each text chunk is converted into a numerical vector representation using an embedding model.

```
Text Chunk → Embedding Model → Vector Representation
```

Embeddings capture the **semantic meaning** of text, allowing the system to compare similarity between queries and document content.

---

### 4. Vector Database Creation

All generated embeddings are stored in a **vector database**.

Examples include:

* Chroma
* FAISS

This database allows fast similarity searches when a user asks a question.

---

### 5. User Question Input

The user interacts with the system through the **Streamlit chatbot interface**.

Example:

```
What are the key announcements in the budget speech?
```

---

### 6. Query Embedding

The user's question is also converted into an embedding using the same embedding model.

```
User Question → Embedding Model → Query Vector
```

This ensures that the query can be compared with document embeddings.

---

### 7. Context Retrieval

The vector database performs a similarity search to retrieve the most relevant document chunks.

```
Query Vector → Vector Search → Top Relevant Chunks
```

These chunks contain the information most likely to answer the user's question.

---

### 8. Chat History Integration

The previous conversation history is added to the prompt so the system remembers earlier interactions.

Example:

```
User: What are the key announcements?
Assistant: ...
User: What about tax changes?
```

This allows the chatbot to support **follow-up questions**.

---

### 9. Prompt Construction

The system constructs a prompt using three elements:

* Retrieved document context
* Chat history
* User question

This structured prompt is then sent to the LLM.

---

### 10. LLM Response Generation

The Large Language Model processes the prompt and generates a response using:

* Retrieved context from the document
* Conversation history
* User question

This produces an **accurate and context-aware answer**.

---

### 11. Response Display

The generated response is displayed in the **Streamlit chatbot interface**, allowing the user to continue the conversation.

---

## 🧠 End-to-End Pipeline

```
PDF Document
      │
      ▼
Text Extraction
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Vector Database
      │
      ▼
User Question
      │
      ▼
Query Embedding
      │
      ▼
Similarity Search
      │
      ▼
Relevant Context
      │
      ▼
Chat History + Context
      │
      ▼
LLM Response
      │
      ▼
Streamlit Chat Interface
```


------------------------------------------------------------------------

# 🚀 How to Run the Project

Clone the repository:

```         
git clone https://github.com/VikramVadhirajan/GenAI_Projects.git
```

Navigate to the project directory:

```         
cd GenAI_Projects/001_RAG_Context_Generation
```

Install dependencies:

```         
pip install -r requirements.txt
```

Launch the notebook:

```         
jupyter notebook
```

Open:

```         
experiments.ipynb
```

Run the notebook cells sequentially to execute the RAG context generation pipeline.

------------------------------------------------------------------------

# 📊 Example Use Cases

Context generation pipelines like this are used in:

-   Document Q&A systems
-   AI knowledge assistants
-   Enterprise search systems
-   Chatbots with knowledge bases
-   AI-powered research tools

------------------------------------------------------------------------

# 🔮 Future Improvements

Planned improvements include:

-   Multi-document context retrieval
-   Hybrid search (vector + keyword)
-   Context ranking and filtering
-   Integration with advanced RAG pipelines

------------------------------------------------------------------------

# 👨‍💻 Author

**Vikram Vadhirajan**

Data Analyst \| Generative AI \| Machine Learning \| Python

GitHub https://github.com/VikramVadhirajan

------------------------------------------------------------------------

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐