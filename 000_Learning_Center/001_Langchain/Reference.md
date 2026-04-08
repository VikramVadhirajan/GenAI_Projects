Components of LangChain

1. Load: Data ingestion Load the data from various source (3.2-DataIngestion.ipynb)
    From Various data source from langchain_community.document_loaders
    https://docs.langchain.com/oss/python/integrations/document_loaders
        TextLoader
        PyPDFLoader
        WebBaseLoader
        ArxivLoader
        WikipediaLoader
    And the  python library requirements for these are 
        langchain-community
        pypdf
        bs4
        arxiv
        PyMuPDF
        wikipedia

2. Split: Split the Text into chunks (chunk_size and chunk_overlap)
    From Various text splitting from langchain_text_splitters
        RecursiveCharacterTextSplitter (text based on the chunk size or double newline)
        CharacterTextSplitter
        HTMLHeaderTextSplitter (Based on header information)
        RecursiveJsonSplitter

    And the  python library requirements for these are 
        langchain-text-splitters

3. Embed The text to vectors so that It can be read by computer
    From Various embedding techniques:
        Open AI from langchain_openai import OpenAIEmbeddings
            (Not free)- Create and manage API Keys from https://platform.openai.com/settings/organization/api-keys
           we can choose model and dimensions from https://developers.openai.com/api/docs/guides/embeddings
            text-embedding-3-large or text-embedding-3-small or text-embedding-ada-002
        Ollama  from langchain_community.embeddings import OllamaEmbeddings
            (Opensource)-download the app and install from https://ollama.com/download/windows
            by default it take llama2 hence one must install it ollama run llama2 in your command line. 
            install needed model ollama run gemma:2b 
            https://ollama.com/blog/embedding-models            
        Huggingface from langchain_huggingface import HuggingFaceEmbeddings
            (Opensoruce) Create an account in  hugging face and create and manage read tokens in https://huggingface.co/settings/tokens
            model_name="all-MiniLM-L6-v2"

    And the  python library requirements for these are 
        langchain-openai
        sentence_transformers
        langchain_huggingface

4. Vector Store  https://docs.langchain.com/oss/python/integrations/vectorstores
    From Various Vector Database from  langchain_community.vectorstores 
        FIASS from langchain_community.vectorstores import FAISS
        Chroma from langchain_chroma import Chroma
    Functions that are in this are 
        .similarity_search()
        .similarity_search_with_score()
        .similarity_search_by_vector()

    And the  python library requirements for these are 
        faiss-cpu
        chromadb
        langchain_chroma

