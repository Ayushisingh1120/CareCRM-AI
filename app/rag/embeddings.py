from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()

    def create_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        embeddings = self.model.encode(texts)

        return embeddings.tolist()