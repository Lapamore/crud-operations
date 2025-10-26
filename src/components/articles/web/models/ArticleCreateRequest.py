from pydantic import BaseModel


class ArticleCreateRequest(BaseModel):
    title: str
    description: str
    body: str
