from pydantic import BaseModel, EmailStr


class ProfileResponse(BaseModel):
    username: str
    email: EmailStr
    bio: str | None = None
    image: str | None = None
