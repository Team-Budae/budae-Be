import json

from openai import OpenAI, OpenAIError

from app.common.exceptions import ValidationError
from app.domains.chat.repository import ChatRepository
from app.domains.chat.schemas import ChatRequest, ChatResponse
from app.domains.place.repository import PlaceRepository
from app.core.config import settings


OPENAI_MODEL = "gpt-5-mini"
DEFAULT_SUGGESTIONS = [
    "서울 관광지 추천해줘",
    "종로구 문화시설 알려줘",
    "한강 근처 데이트 코스 알려줘",
]

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository
        self.place_repository = PlaceRepository(self.repository.session)

    def answer(self, payload: ChatRequest) -> ChatResponse:
        if not payload.message or not payload.message.strip():
            raise ValidationError("메시지를 입력해주세요.")

        session_id = payload.session_id or "default-session"
        self.repository.save_session(session_id)

        user_messages = self._build_message_history(payload.history)
        retrieval_context, sources = self._build_retrieval_context(payload)
        messages = self._build_openai_messages(user_messages, retrieval_context, payload.message)

        answer_text = self._call_openai(messages)

        if not answer_text:
            raise RuntimeError("OpenAI 응답이 비어 있습니다.")

        response = ChatResponse(
            session_id=session_id,
            answer=answer_text,
            sources=sources,
            suggestions=DEFAULT_SUGGESTIONS,
            confidence="high" if sources else "medium",
            used_fallback=False,
        )

        self.repository.append_message(session_id, "user", payload.message)
        self.repository.append_message(session_id, "assistant", response.answer, sources_json=json.dumps(response.sources, ensure_ascii=False))

        return response

    def _build_message_history(self, history: list[dict] | None) -> list[dict]:
        if not history:
            return []

        valid_messages: list[dict] = []
        for item in history:
            role = item.get("role")
            content = item.get("content")
            if role in {"system", "user", "assistant"} and isinstance(content, str) and content.strip():
                valid_messages.append({"role": role, "content": content.strip()})
        return valid_messages

    def _build_retrieval_context(self, payload: ChatRequest) -> tuple[str, list[dict]]:
        keyword = payload.filters.get("keyword") if payload.filters else None
        content_type_id = payload.filters.get("content_type_id") if payload.filters else None
        district = payload.filters.get("district") if payload.filters else None

        if not keyword:
            keyword = self._extract_search_keyword(payload.message)

        places, _ = self.place_repository.search(keyword=keyword, content_type_id=content_type_id)

        sources: list[dict] = []
        if not places:
            return ("", sources)

        snippets = []
        for place in places[:5]:
            snippet = (
                f"[{place.title}] 주소: {place.addr1 or '정보 없음'}",
                f"관할구: {place.district_name or '정보 없음'}",
                f"카테고리: {place.content_type_name or '정보 없음'}",
                f"위치: {place.latitude or '없음'}, {place.longitude or '없음'}",
            )
            snippets.append(" | ".join(snippet))
            sources.append(
                {
                    "title": place.title,
                    "addr1": place.addr1,
                    "district_name": place.district_name,
                    "content_type_name": place.content_type_name,
                    "content_id": place.content_id,
                }
            )

        context_text = (
            "아래는 서울 장소 데이터입니다. 사용자의 질문에 맞춰 해당 정보를 참고해서 답변해 주세요.\n"
            + "\n".join(snippets)
        )
        return (context_text, sources)

    def _extract_search_keyword(self, message: str) -> str | None:
        if "서울" in message or "관광" in message or "추천" in message:
            return "서울"
        return message.strip()

    def _build_openai_messages(self, history_messages: list[dict], context: str, user_message: str) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": (
                    "당신은 서울 관광 정보를 제공하는 LocalHub AI 어시스턴트입니다. "
                    "사용자가 요청한 내용을 이해하고, 가능하면 제공된 장소 데이터를 활용하여 답변하세요. "
                    "출처가 있는 경우 sources 필드에 출처 정보를 포함하고, 답변은 한국어로 간결하게 작성하세요."
                ),
            }
        ]
        messages.extend(history_messages)

        if context:
            messages.append({"role": "system", "content": context})

        messages.append({"role": "user", "content": user_message})
        return messages

    def _call_openai(self, messages: list[dict]) -> str:
        try:
            print("===== OpenAI Request =====")
            print(messages)

            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_completion_tokens=800,
            )

            print("===== OpenAI Response =====")
            print(response)

            content = response.choices[0].message.content

            if not content:
                print("OpenAI returned empty content")
                return ""

            return content.strip()

        except Exception as e:
            import traceback
            traceback.print_exc()
            return ""
