from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_documents(file_paths):
    docs = []
    for path in file_paths:
        ext = path.split('.')[-1].lower()
        if ext == 'pdf':
            loader = PyPDFLoader(path)
        elif ext == 'txt':
            loader = TextLoader(path)
        else:
            print(f"Unsupported file type: {ext} for file {path}, skipping.")
            continue
        docs.extend(loader.load())
    return docs


def create_vector_store(docs, embeddings):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(docs)

    from langchain_community.vectorstores import FAISS
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore
