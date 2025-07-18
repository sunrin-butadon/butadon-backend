from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.password import hash_password, verify_password
from app.core.auth import create_access_token, verify_access_token, get_current_user, TokenPayload
from app.db.deps import get_db, get_chroma_client
import app.api.users.users_dto as dto
import app.api.users.users_crud as crud

router = APIRouter()

@router.get("/{user_id}/info/", response_model=dto.UserInfoDTO, tags=["users"])
async def get_users(
    user_id: str,
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return dto.UserInfoDTO(
        cuid=user.cuid,
        username=user.username,
        email=user.email
    )


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
    token_payload = TokenPayload(sub=user.cuid, role="user")
    access_token = create_access_token(data=token_payload)

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

@router.put("/profile", response_model=dto.UserResponseDTO, tags=["users"])
async def update_user_profile(
    item: dto.UserUpdateDTO,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 프로필을 업데이트합니다."""
    updated_user = crud.update_user(current_user["sub"], item, db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/profile", response_model=dto.UserProfileDTO, tags=["users"])
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 프로필과 생성/북마크한 항목들을 조회합니다."""
    profile = crud.get_user_profile(current_user["sub"], db)
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

@router.post("/bookmarks/datasets/{dataset_id}", tags=["users"])
async def bookmark_dataset(
    dataset_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """데이터셋을 북마크합니다."""
    success = crud.add_bookmarked_dataset(current_user["sub"], dataset_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Dataset bookmarked successfully"}

@router.delete("/bookmarks/datasets/{dataset_id}", tags=["users"])
async def unbookmark_dataset(
    dataset_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """데이터셋 북마크를 제거합니다."""
    success = crud.remove_bookmarked_dataset(current_user["sub"], dataset_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Dataset bookmark removed successfully"}

@router.post("/bookmarks/rags/{rag_id}", tags=["users"])
async def bookmark_rag(
    rag_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RAG를 북마크합니다."""
    success = crud.add_bookmarked_rag(current_user["sub"], rag_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "RAG bookmarked successfully"}

@router.delete("/bookmarks/rags/{rag_id}", tags=["users"])
async def unbookmark_rag(
    rag_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """RAG 북마크를 제거합니다."""
    success = crud.remove_bookmarked_rag(current_user["sub"], rag_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "RAG bookmark removed successfully"}
