from xml.dom.minidom import Document
from chromadb import URI, Embeddings, IDs, Include
import numpy as np
from pydantic import BaseModel, validator, Field
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
    username: Optional[str] = None  # User 이름
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
    answer: str = Field(
        example="질문에 대한 RAG를 사용한 답변")
    
class RagBuildResponseDTO(BaseModel):
    message: str = Field(
        example="RAG 벡터 데이터베이스가 성공적으로 구축되었습니다."
    )

    
class RagDocumentSearchResponseDTO(BaseModel):
    ids: List[List[str]] = Field(
        example=[
            [
                "38cd5a6e-bbff-4631-a7a2-11ba811b81f2_5",
                "38cd5a6e-bbff-4631-a7a2-11ba811b81f2_4",
                "38cd5a6e-bbff-4631-a7a2-11ba811b81f2_11",
                "38cd5a6e-bbff-4631-a7a2-11ba811b81f2_15",
                "38cd5a6e-bbff-4631-a7a2-11ba811b81f2_6"
            ]
        ]
    )
    embeddings: Optional[List[List[float]]] = Field(None, example=None)
    documents: List[List[str]] = Field(
        example=[
            [
                " 부원이 모두 모여 Git/Github에 대한 수업을 들었습니다. 수업의 진행은 PARA의 2학년㏗김현호㏘ 부원이 진행했습니다. VCS의 개념, Git의 구성, Github를 사용한 Git 실습, 웹 페이지 제작 팀프로젝트 등의 수업을 진행했습니다.",
                "세와 주의점들을 안내했습니다. 특히, 교우관계에 대한 조언과 전공 공부 및 학업에 대한 다양한 방향을 제시해주었습니다.",
                " 글로벌 챌린지 ㎿ 곽원영 2. 2024 사이버공격방어대회 ㎿ 이정훈 3. 2024 한국코드페어 SW공모전 ㎿ 이정훈, 김가온 4. 2024 암호분석경진대회 ㎿ 이정훈",
                "대한 내용을 과하게 추상화했고, 이는 실습 내용에 대한 제한으로 이어졌습니다. 결국 나중엔 무료 코랩에서 LLM을 파인튜닝하기 위해서 시스템 자원을 절약하는 온갖 방법론을 동원한 라이브러리인 unsloth를 사용하여 Llama㎽3㎽8b 모델을 파인튜닝할 수 있었습니다.",
                " Transformer 모델을 불러오는 과정은 HuggingFace에 대해서 설명하고 HuggingFace에 공개된 모델을 불러와 사용했습니다."
            ]
        ]
    )
    uris: Optional[List[List[str]]] = Field(None, example=None)
    included: List[str] = Field(
        example=["metadatas", "documents", "distances"]
    )
    data: Optional[dict] = Field(None, example=None)
    metadatas: Optional[List[List[Optional[dict]]]] = Field(
        None,
        example=[
            [None, None, None, None, None]
        ]
    )
    distances: Optional[List[List[float]]] = Field(
        None,
        example=[
            [
                1.5281548500061035,
                1.5323833227157593,
                1.5814175605773926,
                1.5871717929840088,
                1.61759352684021
            ]
        ]
    )