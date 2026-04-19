import streamlit as st
import tempfile

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


st.set_page_config(page_title="PDF Q&A with Groq", layout="wide")

st.title("📄 Ask Questions From Your PDF (Groq + LangChain)")


# -------------------------------
# SESSION STATE
# -------------------------------

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None


# -------------------------------
# USER INPUT
# -------------------------------
st.sidebar.title("User Inputs")
groq_api_key = st.sidebar.text_input(
    "Enter your GROQ API Key",
    type="password"
)

uploaded_pdf = st.sidebar.file_uploader(
    "Upload a PDF file",
    type="pdf"
)


# -------------------------------
# VECTOR DATABASE CREATION
# -------------------------------

@st.cache_resource
def build_vector_store(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(split_docs, embeddings)

    return vector_db


# -------------------------------
# PROCESS PDF ONLY ONCE
# -------------------------------

if uploaded_pdf and groq_api_key:

    if st.session_state.vector_db is None:

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            pdf_path = tmp_file.name

        with st.spinner("Processing PDF and creating vector database..."):

            vector_db = build_vector_store(pdf_path)

            st.session_state.vector_db = vector_db
            st.session_state.retriever = vector_db.as_retriever(search_kwargs={"k": 4})

        st.success("✅ PDF processed successfully!")

    retriever = st.session_state.retriever


    # -------------------------------
    # GROQ MODEL
    # -------------------------------

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model="openai/gpt-oss-120b"
    )


    # -------------------------------
    # PROMPT
    # -------------------------------

    template = """
You are an AI assistant. Answer the question using ONLY the context provided.

Context:
{context}

Question:
{question}

Answer clearly.
"""

    prompt = ChatPromptTemplate.from_template(template)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )


    # -------------------------------
    # QUESTION INPUT
    # -------------------------------

    question = st.text_input("Ask a question about the PDF")

    if question:

        with st.spinner("Generating answer..."):

            answer = rag_chain.invoke(question)

        st.markdown("### 📌 Answer")
        st.write(answer)

else:

    st.info("Enter your GROQ API key and upload a PDF to start.")