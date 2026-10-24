from pathlib import Path

from app.rag.document_loader import load_markdown
from app.rag.chunker import chunk_text
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


BASE_DIR = Path(__file__).resolve().parent.parent

file_path = (
    BASE_DIR
    / "data"
    / "knowledge_base"
    / "support_policy.md"
)


print("Loading document...")

content = load_markdown(str(file_path))

print(f"Document loaded: {len(content)} characters")


print("Creating chunks...")

chunks = chunk_text(
    content,
    chunk_size=500,
    chunk_overlap=100
)

print(f"Created {len(chunks)} chunks")


print("Creating embeddings...")

embedding_service = EmbeddingService()

embeddings = embedding_service.create_embeddings(
    chunks
)

print(
    f"Created {len(embeddings)} embeddings"
)


print("Storing in ChromaDB...")

vector_store = VectorStore()

ids = [
    f"support_policy_{index}"
    for index in range(len(chunks))
]

metadatas = [
    {
        "source": "support_policy.md",
        "chunk_index": index
    }
    for index in range(len(chunks))
]

vector_store.add_documents(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)

print(
    f"Knowledge base indexed successfully!"
)

print(
    f"Total vectors in ChromaDB: "
    f"{vector_store.count()}"
)