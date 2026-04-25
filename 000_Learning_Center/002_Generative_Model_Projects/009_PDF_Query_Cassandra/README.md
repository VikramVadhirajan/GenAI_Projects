# 📄 PDF Query System using LangChain + Cassandra

## 🚀 Overview
This project enables querying PDF documents using LangChain by:
- Extracting text from PDFs
- Splitting text into chunks
- Generating embeddings
- Storing vectors in Cassandra
- Querying using an LLM

---

## 🧠 Tech Stack
- LangChain
- OpenAI
- PyPDF2
- Cassandra (via CassIO)
- Hugging Face Datasets

---

## ⚙️ Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Environment
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
```

If using Astra DB:

```env
ASTRA_DB_APPLICATION_TOKEN=your_token
ASTRA_DB_ID=your_db_id
```

---

## ▶️ How to Run

```bash
jupyter notebook
```

Open:
```
PDFQuery_LangChain.ipynb
```

Run all cells step by step.

---

## 📂 Project Structure

```
.
├── PDFQuery_LangChain.ipynb
├── requirements.txt
├── README.md
└── .env
```

---

## 🔍 Workflow

1. Load PDF using PyPDF2
2. Split text using LangChain splitter
3. Generate embeddings (OpenAI)
4. Store in Cassandra vector DB
5. Query using LLM

---

## ⚠️ Common Issues

### ❌ OpenAI Error
- Ensure API key is set properly

### ❌ Cassandra Connection Error
- Verify Astra DB credentials
- Ensure network access is enabled

### ❌ Token Limit Issues
- Reduce chunk size in text splitter

---

## 📈 Future Improvements
- Add Streamlit UI
- Support multiple PDFs
- Use local LLM instead of OpenAI
- Add semantic search optimization

---

## 👨‍💻 Author
Your Name
