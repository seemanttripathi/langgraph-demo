from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

QDRANT_PATH = "qdrant_data"
COLLECTION_NAME = "research_knowledge"

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

def get_vector_store():
    return QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )

def retrieve(query: str, k: int = 3):
    vector_store = get_vector_store()

    result = vector_store.similarity_search(
        query,
        k=k,
    )

    return result

if __name__ == "__main__":
    query = "What is Retrieval-Augmented Generation?"

    results = retrieve(query, k=3)

    for i, doc in enumerate(results, start=1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {doc.metadata.get('source')}")
        print(doc.page_content)