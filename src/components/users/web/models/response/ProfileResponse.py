from pydantic import BaseModel
from typing import Optional


class ProfileResponse(BaseModel):
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None
