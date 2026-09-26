from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

DATA_DIR = Path("data")
QDRANT_PATH = "qdrant_data"
COLLECTION_NAME = "research_knowledge"

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

def load_documents():
    documents = []
    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name
                },
            )
        )
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    return splitter.split_documents(documents)

def build_vector_store():
    documents = load_documents()

    chunks = split_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )

    print("Documents indexed successfully.")

    return vector_store

if __name__ == "__main__":
    build_vector_store()