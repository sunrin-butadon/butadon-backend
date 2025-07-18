from sqlalchemy.orm import Session
import json

from app.db.deps import get_db
from app.core.password import hash_password
from app.api.users.users_model import User
import app.api.users.users_dto as dto

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: str, db: Session):
    return db.query(User).filter(User.cuid == user_id).first()

def register_user(item: dto.UserCreateDTO, db: Session):
    db_user = User(
        username=item.username,
        email=item.email,
        hashed_password=hash_password(item.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return dto.UserResponseDTO(
        cuid=db_user.cuid,
        username=db_user.username,
        email=db_user.email
    )

def update_user(user_id: str, item: dto.UserUpdateDTO, db: Session):
    """사용자 기본 정보를 업데이트합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return None
    
    if item.username is not None:
        db_user.username = item.username
    if item.email is not None:
        db_user.email = item.email
    if item.password is not None:
        db_user.hashed_password = hash_password(item.password)
    
    db.commit()
    db.refresh(db_user)
    
    return dto.UserResponseDTO(
        cuid=db_user.cuid,
        username=db_user.username,
        email=db_user.email
    )

def get_user_profile(user_id: str, db: Session):
    """사용자 프로필과 생성/북마크한 항목들을 조회합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return None
    
    return dto.UserProfileDTO(
        cuid=db_user.cuid,
        username=db_user.username,
        email=db_user.email,
        created_dataset_ids=json.loads(db_user.created_dataset_ids or "[]"),
        bookmarked_dataset_ids=json.loads(db_user.bookmarked_dataset_ids or "[]"),
        created_rag_ids=json.loads(db_user.created_rag_ids or "[]"),
        bookmarked_rag_ids=json.loads(db_user.bookmarked_rag_ids or "[]")
    )

def add_created_dataset(user_id: str, dataset_id: str, db: Session):
    """사용자가 생성한 데이터셋 ID를 추가합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_dataset_ids or "[]")
    if dataset_id not in created_ids:
        created_ids.append(dataset_id)
        db_user.created_dataset_ids = json.dumps(created_ids)
        db.commit()
    
    return True

def remove_created_dataset(user_id: str, dataset_id: str, db: Session):
    """사용자가 생성한 데이터셋 ID를 제거합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_dataset_ids or "[]")
    if dataset_id in created_ids:
        created_ids.remove(dataset_id)
        db_user.created_dataset_ids = json.dumps(created_ids)
        db.commit()
    
    return True

def add_bookmarked_dataset(user_id: str, dataset_id: str, db: Session):
    """사용자가 북마크한 데이터셋 ID를 추가합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    bookmarked_ids = json.loads(db_user.bookmarked_dataset_ids or "[]")
    if dataset_id not in bookmarked_ids:
        bookmarked_ids.append(dataset_id)
        db_user.bookmarked_dataset_ids = json.dumps(bookmarked_ids)
        db.commit()
    
    return True

def remove_bookmarked_dataset(user_id: str, dataset_id: str, db: Session):
    """사용자가 북마크한 데이터셋 ID를 제거합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    bookmarked_ids = json.loads(db_user.bookmarked_dataset_ids or "[]")
    if dataset_id in bookmarked_ids:
        bookmarked_ids.remove(dataset_id)
        db_user.bookmarked_dataset_ids = json.dumps(bookmarked_ids)
        db.commit()
    
    return True

def add_created_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 생성한 RAG ID를 추가합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_rag_ids or "[]")
    if rag_id not in created_ids:
        created_ids.append(rag_id)
        db_user.created_rag_ids = json.dumps(created_ids)
        db.commit()
    
    return True

def remove_created_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 생성한 RAG ID를 제거합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_rag_ids or "[]")
    if rag_id in created_ids:
        created_ids.remove(rag_id)
        db_user.created_rag_ids = json.dumps(created_ids)
        db.commit()
    
    return True

def add_bookmarked_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 북마크한 RAG ID를 추가합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    bookmarked_ids = json.loads(db_user.bookmarked_rag_ids or "[]")
    if rag_id not in bookmarked_ids:
        bookmarked_ids.append(rag_id)
        db_user.bookmarked_rag_ids = json.dumps(bookmarked_ids)
        db.commit()
    
    return True

def remove_bookmarked_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 북마크한 RAG ID를 제거합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    bookmarked_ids = json.loads(db_user.bookmarked_rag_ids or "[]")
    if rag_id in bookmarked_ids:
        bookmarked_ids.remove(rag_id)
        db_user.bookmarked_rag_ids = json.dumps(bookmarked_ids)
        db.commit()
    
    return True


def add_created_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 생성한 RAG ID를 추가합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_rag_ids or "[]")
    if rag_id not in created_ids:
        created_ids.append(rag_id)
        db_user.created_rag_ids = json.dumps(created_ids)
        db.commit()
    
    return True


def remove_created_rag(user_id: str, rag_id: str, db: Session):
    """사용자가 생성한 RAG ID를 제거합니다."""
    db_user = get_user_by_id(user_id, db)
    if not db_user:
        return False
    
    created_ids = json.loads(db_user.created_rag_ids or "[]")
    if rag_id in created_ids:
        created_ids.remove(rag_id)
        db_user.created_rag_ids = json.dumps(created_ids)
        db.commit()
    
    return True

