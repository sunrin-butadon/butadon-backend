from sqlalchemy.orm import Session
import datetime
import uuid

from app.db.deps import get_db
from app.api.datasets.datasets_model import Dataset
import app.api.datasets.datasets_dto as dto

def create_dataset(item: dto.DatasetCreateDTO, user_id: str, file_type: str, db: Session):
    dataset = Dataset(
        name=item.name,
        made_by_user=user_id,
        description=item.description,
        file_type=file_type,
        created_at=datetime.datetime.now().isoformat()
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dto.DatasetResponseDTO(
        id=dataset.id,
        name=dataset.name,
        made_by_user=dataset.made_by_user,
        description=dataset.description,
        file_type=dataset.file_type,
        created_at=dataset.created_at)

def get_dataset_by_id(dataset_id: str, db: Session) -> Dataset:
    """
    데이터셋 ID로 데이터셋을 조회합니다.
    """
    return db.query(Dataset).filter(Dataset.id == dataset_id).first()

def get_dataset_list(db: Session):
    """
    데이터셋 목록을 조회합니다.
    """
    return db.query(Dataset).all()