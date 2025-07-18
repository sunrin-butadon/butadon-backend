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



@router.post("/{rag_id}/build_db", tags=["rags"])
async def build_rag_db(
    rag_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    rag = crud.get_rag_by_id(rag_id, db)
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    
    if rag.made_by_user != current_user['id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다.")
    
    build_result = build_db(rag_id, db)
    
    if not build_result:
        raise HTTPException(status_code=500, detail="벡터 데이터베이스 구축에 실패했습니다.")
    
    return {"message": "RAG 벡터 데이터베이스가 성공적으로 구축되었습니다."}

@router.post("/document_search", tags=["rags"])
async def search_rag_documents(
    item: dto.RagDocumentSearchDTO,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    rag = crud.get_rag_by_id(item.rag_id, db)
    
    if not rag:
        raise HTTPException(status_code=404, detail="RAG를 찾을 수 없습니다.")
    
    
    return chroma_client.search_by_embedding(chroma_client.get_chroma_collection_name(rag_id=item.rag_id),chroma_client._get_embedding(item.query))