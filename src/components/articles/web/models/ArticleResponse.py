from typing import List, Optional
from pydantic import BaseModel
from components.users.web.models.response.ProfileResponse import ProfileResponse


class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None
    author: ProfileResponse
