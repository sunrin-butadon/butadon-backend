from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.password import hash_password, verify_password
from app.core.auth import create_access_token, verify_access_token, get_current_user
from app.db.deps import get_db, get_chroma_client
import app.api.users.users_dto as dto
import app.api.users.users_crud as crud

router = APIRouter()

@router.post("/register", response_model=dto.UserResponseDTO, tags=["users"])
async def register_user(item:dto.UserCreateDTO, db: Session = Depends(get_db)):
    # 이메일 중복확인
    if crud.get_user_by_email(item.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        res:dto.UserResponseDTO = crud.register_user(item, db)
        return res
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"User registration failed: {str(e)}")
    
@router.post("/login", tags=["users"])
async def login_user(item: dto.UserLoginDTO, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(item.email, db)

    if not user or not verify_password(item.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # 로그인 성공 시 JWT 토큰 발급
    access_token = create_access_token(data={"sub": user.cuid, "role": "user"})

    return dto.TokenResponseDTO(
        access_token=access_token,
        token_type="bearer",
        user=dto.UserResponseDTO(
            cuid=user.cuid,
            username=user.username,
            email=user.email
        )   
    )
    

@router.get("/verify", tags=["users"])
async def verify_user(current_user: Session = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = crud.get_user_by_id(current_user["sub"], db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return dto.UserResponseDTO(
        cuid=user.cuid,
        username=user.username,
        email=user.email
    )
