from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    tag: Mapped[str]
