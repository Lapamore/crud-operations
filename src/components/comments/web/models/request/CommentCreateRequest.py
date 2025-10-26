from pydantic import BaseModel


class CommentCreateRequest(BaseModel):
    body: str
