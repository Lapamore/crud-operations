from pydantic import BaseModel
from components.users.web.models.response.ProfileResponse import ProfileResponse


class CommentResponse(BaseModel):
    id: int
    body: str
    author: ProfileResponse
