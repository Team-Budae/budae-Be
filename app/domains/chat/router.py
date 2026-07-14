from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.chat.repository import ChatRepository
from app.domains.chat.schemas import ChatRequest, ChatResponse
from app.domains.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    repository = ChatRepository(db)
    return ChatService(repository)


@router.post("", response_model=ChatResponse, summary="챗봇 질의 응답")
async def chat(payload: ChatRequest, service: ChatService = Depends(get_chat_service)):
    return service.answer(payload)
