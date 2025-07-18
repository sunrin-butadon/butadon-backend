from xml.dom.minidom import Document
from chromadb import URI, Embeddings, IDs, Include
import numpy as np
from pydantic import BaseModel, validator
from typing import Optional, List, Union
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

class RagQuestionDTO(BaseModel):
    rag_id: str
    question: str
    top_k: int = 5

class RagQuestionResponseDTO(BaseModel):
    answer: str
    
class RagBuildResponseDTO(BaseModel):
    message: str

    
class RagDocumentSearchResponseDTO(BaseModel):
    ids: List[List[str]]
    embeddings: Optional[List[List[float]]] = None
    documents: List[List[str]]
    uris: Optional[List[List[str]]] = None
    included: List[str]
    data: Optional[dict] = None
    metadatas: Optional[List[List[Optional[dict]]]] = None
    distances: Optional[List[List[float]]] = None