from sqlalchemy.orm import Session

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

