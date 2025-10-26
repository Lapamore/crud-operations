from pydantic import BaseModel, EmailStr
from typing import Optional


class UserResponse(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None