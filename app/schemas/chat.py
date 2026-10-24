from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    chunk_index: int
    distance: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]