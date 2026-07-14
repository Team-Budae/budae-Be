from app.common.exceptions import ValidationError
from app.domains.chat.repository import ChatRepository
from app.domains.chat.schemas import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    def answer(self, payload: ChatRequest) -> ChatResponse:
        if not payload.message.strip():
            raise ValidationError("메시지를 입력해주세요.")

        session_id = payload.session_id or "default-session"
        self.repository.save_session(session_id)

        answer = "현재는 서울 관광 데이터 기반의 기본 응답 구조만 준비되어 있습니다."
        response = ChatResponse(
            session_id=session_id,
            answer=answer,
            sources=[],
            suggestions=["서울 관광지 추천해줘", "종로구 문화시설 알려줘"],
            confidence="medium",
            used_fallback=True,
        )

        self.repository.append_message(session_id, "user", payload.message)
        self.repository.append_message(session_id, "assistant", response.answer, sources_json="[]")
        return response
