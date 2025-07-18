from pydantic import BaseModel, Field, EmailStr



class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserLoginDTO(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8)

class UserResponseDTO(BaseModel):
    cuid: str = Field(..., alias="cuid")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., max_length=100) 

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseDTO