from sqlalchemy import Column, String
from sqlalchemy.orm import Session
import datetime
import uuid
import json

from app.api.rags.rags_model import RagModel
import app.api.rags.rags_dto as dto
import app.api.users.users_crud as users_crud


def create_rag(item: dto.RagCreateDTO, user_id: str, db: Session):
    rag_id = str(uuid.uuid4())
    
    # RAG DB 모델
    db_rag = RagModel(
        id=rag_id,
        name=item.name,
        description=item.description,

        made_by_user=user_id,
        created_at=datetime.datetime.now().isoformat(),

        dataset_ids=json.dumps(item.dataset_ids),  # JSON 문자열로 변환
        llm_model=item.llm_model,
        chunk_size=item.chunk_size
    )
    
    db.add(db_rag)
    db.commit()
    db.refresh(db_rag)
    
    users_crud.add_created_rag(user_id, rag_id, db)
    
    return db_rag

def get_rag_by_id(rag_id: str, db: Session) -> RagModel:
    """
    RAG ID로 RAG를 조회합니다.
    """
    return db.query(RagModel).filter(RagModel.id == rag_id).first()

def get_rags_list(db: Session):
    return db.query(RagModel).all()