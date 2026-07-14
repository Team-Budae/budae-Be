from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str
    history: list[dict] | None = None
    filters: dict | None = None


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    answer: str
    sources: list[dict] = []
    suggestions: list[str] = []
    confidence: str = "medium"
    used_fallback: bool = False
