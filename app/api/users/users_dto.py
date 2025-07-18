from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserLoginDTO(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserUpdateDTO(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)

class UserResponseDTO(BaseModel):
    cuid: str = Field(..., alias="cuid")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)

class UserProfileDTO(BaseModel):
    cuid: str
    username: str
    email: EmailStr
    created_dataset_ids: List[str] = []
    bookmarked_dataset_ids: List[str] = []
    created_rag_ids: List[str] = []
    bookmarked_rag_ids: List[str] = []

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDTO