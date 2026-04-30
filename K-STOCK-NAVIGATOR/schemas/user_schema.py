from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=20)
    password: str = Field(..., min_length=8) # 8자 이상 필수

class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
