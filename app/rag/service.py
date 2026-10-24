from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.llm.client import LLMClient


class RAGService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm = LLMClient()

    def retrieve(self, question: str, top_k: int = 3) -> dict:

        query_embedding = self.embedding_service.create_embedding(
            question
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return {
                "documents": [],
                "sources": []
            }

        sources = []

        for index, metadata in enumerate(metadatas):
            sources.append({
                "source": metadata.get("source"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distances[index]
            })

        return {
            "documents": documents,
            "sources": sources
        }

    def answer(self, question: str, top_k: int = 3) -> dict:

        results = self.retrieve(
            question=question,
            top_k=top_k
        )

        documents = results["documents"]
        sources = results["sources"]

        if not documents:
            return {
                "answer": "I could not find relevant information in the knowledge base.",
                "sources": []
            }

        context_parts = []

        for index, document in enumerate(documents):
            context_parts.append(
                f"[Source {index + 1}]\n{document}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are CareCRM AI, a customer support assistant.

Answer the user's question using ONLY the provided knowledge base context.

If the context does not contain enough information to answer,
say that you do not have enough information.

Do not invent policies, facts, or promises.

Knowledge Base Context:
------------------------
{context}
------------------------

User Question:
{question}

Provide a clear and concise answer.
"""

        answer = self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": sources
        }