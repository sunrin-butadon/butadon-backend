from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import json


class RagCreateDTO(BaseModel):
    name: str
    description: Optional[str] = None
    dataset_ids: List[str]
    chunk_size: int
    llm_model: str # OpenAI 모델 이름

class RagResponseDTO(BaseModel):

    
    id: str

    name: str
    description: Optional[str] = None
    made_by_user: str  # User CUID
    created_at: datetime  # ISO format string
    
    dataset_ids: List[str]
    llm_model: str
    chunk_size: int

    @validator('dataset_ids', pre=True)
    def parse_dataset_ids(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    @validator('created_at', pre=True)
    def parse_created_at(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v

    class Config:
        from_attributes = True



class RagDocumentSearchDTO(BaseModel):
    rag_id: str
    query: str
    top_k: int = 5