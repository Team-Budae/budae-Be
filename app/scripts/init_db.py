from app.core.database import Base, engine
from app.domains.category.models import Category
from app.domains.chat.models import ChatMessage, ChatSession
from app.domains.comment.models import Comment
from app.domains.data_source.models import DataSource
from app.domains.place.models import Place
from app.domains.post.models import Post


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized")
