from sqlalchemy.orm import Session

from app.common.repository import BaseRepository
from app.domains.chat.models import ChatMessage, ChatSession


class ChatRepository(BaseRepository[ChatMessage]):
    def __init__(self, session: Session):
        super().__init__(session, ChatMessage)

    def save_session(self, session_id: str) -> ChatSession:
        chat_session = self.session.get(ChatSession, session_id)
        if not chat_session:
            chat_session = ChatSession(id=session_id)
            self.session.add(chat_session)
            self.session.commit()
        return chat_session

    def append_message(self, session_id: str, role: str, content: str, sources_json: str | None = None) -> ChatMessage:
        message = ChatMessage(session_id=session_id, role=role, content=content, sources_json=sources_json)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message
