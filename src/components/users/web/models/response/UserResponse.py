from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    token: str