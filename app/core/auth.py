from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from app.core.config import settings


class TokenPayload(BaseModel):
    sub: str
    role: str
    
bearer_scheme = HTTPBearer()


def create_access_token(data: TokenPayload) -> str:
    to_encode = data.model_dump()  # Pydantic 모델을 딕셔너리로 변환
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    payload = verify_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return payload