from typing import List, Optional
from pydantic import BaseModel


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tagList: Optional[List[str]] = None
