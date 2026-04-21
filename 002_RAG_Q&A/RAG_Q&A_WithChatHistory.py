import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
import tempfile
import os

st.set_page_config(page_title="PDF Chatbot with Groq", layout="wide")

st.title("📄 Chat with your PDF (Groq + LangChain)")

# -------------------------
# Session State
# -------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processed" not in st.session_state:
    st.session_state.processed = False


# -------------------------
# Sidebar Inputs
# -------------------------

st.sidebar.header("Configuration")

groq_key = st.sidebar.text_input("Enter Groq API Key", type="password")

uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF",
    type="pdf"
)


# -------------------------
# PDF Processing
# -------------------------

def process_pdf(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


# -------------------------
# Build Vector DB
# -------------------------

if uploaded_pdf and not st.session_state.processed:

    with st.spinner("Processing PDF and creating vector database..."):

        st.session_state.vectorstore = process_pdf(uploaded_pdf)

        st.session_state.processed = True

    st.success("PDF processed successfully!")


# -------------------------
# Chat Interface
# -------------------------

if st.session_state.vectorstore and groq_key:

    llm = ChatGroq(
        groq_api_key=groq_key,
        model_name="openai/gpt-oss-120b",
        temperature=0
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        st.session_state.vectorstore.as_retriever(),
        return_source_documents=True
    )

    question = st.chat_input("Ask a question about the PDF")

    if question:

        result = qa_chain.invoke({
            "question": question,
            "chat_history": st.session_state.chat_history
        })

        answer = result["answer"]

        st.session_state.chat_history.append((question, answer))


    # Display chat history
    for q, a in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(q)

        with st.chat_message("assistant"):
            st.write(a)


else:
    st.info("Upload a PDF and enter your Groq API key to start chatting.")