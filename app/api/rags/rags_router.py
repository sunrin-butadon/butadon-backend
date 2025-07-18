from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel
import json


from app.db.deps import get_db
from app.core.auth import get_current_user
import app.api.rags.rags_crud as crud
import app.api.rags.rags_dto as dto

from app.services.rags.build_db import build_db
from app.db.chroma.client import chroma_client

router = APIRouter()


@router.post("/create", tags=["rags"], response_model=dto.RagResponseDTO)
async def create_rag(
    item: dto.RagCreateDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rag = crud.create_rag(item, current_user['id'], db)
    return rag

@router.get("/list", tags=["rags"], response_model=List[dto.RagResponseDTO])
async def list_rags(db: Session = Depends(get_db)):

    rags = crud.get_rags_list(db)
    return rags

@router.get("/{rag_id}", tags=["rags"], response_model=dto.RagResponseDTO)
async def get_rag(rag_id: str, db: Session = Depends(get_db)):

    rag = crud.get_rag_by_id(rag_id, db)
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    return rag



@router.post("/{rag_id}/build", tags=["rags"], response_model=dto.RagBuildResponseDTO)
async def build_rag_db(
    rag_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rag = crud.get_rag_by_id(rag_id, db)
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    
    if rag.made_by_user != current_user['id']:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    build_result = build_db(rag_id, db)
    
    if not build_result:
        raise HTTPException(status_code=500, detail="벡터 데이터베이스 구축에 실패했습니다.")
    
    return {"message": "RAG 벡터 데이터베이스가 성공적으로 구축되었습니다."}

@router.post("/document_search", tags=["rags"], response_model=dto.RagDocumentSearchResponseDTO)
async def search_rag_documents(
    item: dto.RagDocumentSearchDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rag = crud.get_rag_by_id(item.rag_id, db)
    
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    
    
    return chroma_client.search_by_embedding(chroma_client.get_chroma_collection_name(rag_id=item.rag_id),chroma_client._get_embedding(item.query))


@router.get("/{rag_id}/question_answer", tags=["rags"], response_model=dto.RagQuestionResponseDTO)
async def rag_question_answer(
    rag_id: str,
    question: str,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    RAG를 사용하여 질문에 대한 답변을 생성합니다.
    """
    rag = crud.get_rag_by_id(rag_id, db)
    
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    
    # RAG 벡터 데이터베이스에서 문서 검색
    search_results = chroma_client.search_by_embedding(
        chroma_client.get_chroma_collection_name(rag_id=rag_id),
        chroma_client._get_embedding(question)
    )
    
    if not search_results or not search_results['documents']:
        raise HTTPException(status_code=404, detail="관련 문서를 찾을 수 없습니다.")
    
    # 검색 결과를 평탄화하여 문자열로 변환
    documents = []
    for doc_list in search_results['documents']:
        documents.extend(doc_list)
    
    # OpenAI API를 사용하여 답변 생성
    response = chroma_client.openai_client.chat.completions.create(
        model=rag.llm_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": "\n".join(documents)}
        ]
    )
    
    return {"answer": response.choices[0].message.content}