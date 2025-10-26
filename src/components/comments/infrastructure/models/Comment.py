from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from infrastructure.db.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id})>"
