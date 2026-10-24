from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


embedding_service = EmbeddingService()
vector_store = VectorStore()


query = "Can a support agent promise a refund?"


print(f"Query: {query}")
print("\nCreating query embedding...")

query_embedding = embedding_service.create_embedding(
    query
)


print("Searching ChromaDB...\n")

results = vector_store.search(
    query_embedding=query_embedding,
    top_k=3
)


documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]
distances = results.get("distances", [[]])[0]


for index, document in enumerate(documents):

    print(f"--- Result {index + 1} ---")

    print("Document:")
    print(document)

    print("\nMetadata:")
    print(metadatas[index])

    print("\nDistance:")
    print(distances[index])

    print()
    