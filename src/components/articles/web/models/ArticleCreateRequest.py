from typing import List, Optional
from pydantic import BaseModel


class ArticleCreateRequest(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None
