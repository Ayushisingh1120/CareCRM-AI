from pathlib import Path

import chromadb

from app.core.config import settings


class VectorStore:
    def __init__(self):
        chroma_path = Path("data/chroma")

        chroma_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.client = chromadb.PersistentClient(
            path=str(chroma_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection
        )

    def add_documents(
        self,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str]
    ):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

    def count(self) -> int:
        return self.collection.count()