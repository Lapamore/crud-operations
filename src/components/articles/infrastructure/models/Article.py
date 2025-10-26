from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship

from infrastructure.db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Article(title='{self.title}')>"
