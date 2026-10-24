from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.service import RAGService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


rag = RAGService()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        result = rag.answer(request.question)

        return {
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )