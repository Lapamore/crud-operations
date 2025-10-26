from typing import Optional
from pydantic import EmailStr, BaseModel


class UserUpdateRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    bio: Optional[str] = None 
    image: Optional[str] = None