from app.db.chroma.client import ChromaDBClient
from app.core.config import settings
from app.api.rags.rags_crud import get_rag_by_id
from app.api.datasets.datasets_crud import get_dataset_by_id
from app.db.deps import get_db
from sqlalchemy.orm import Session
import json
import PyPDF2
import os
from typing import List

chroma_client = ChromaDBClient()

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """텍스트를 청크로 분할합니다."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    return chunks

def read_pdf_content(file_path: str) -> str:
    """PDF 파일의 내용을 읽어옵니다."""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def build_db(rag_id: str, db: Session):
    """
    RAG 벡터 데이터베이스를 구축합니다.
    """
    # ChromaDB에서 RAG 컬렉션 이름 가져오기
    collection_name = chroma_client.get_chroma_collection_name(rag_id)
    
    chroma_client.create_or_get_collection(collection_name)

    # get_rag_by_id 로 RAG 정보 가져오기
    rag = get_rag_by_id(rag_id, db)
    dataset_ids = json.loads(rag.dataset_ids)
    
    # get_dataset_by_id 로 데이터셋 정보 가져오기
    all_documents = []
    all_embeddings = []
    all_ids = []
    
    for dataset_id in dataset_ids:
        dataset = get_dataset_by_id(dataset_id, db)
        
        # 데이터셋 파일 읽기
        file_path = f"./uploads/datasets/{dataset_id}.{dataset.file_type}"
        
        if dataset.file_type == 'pdf':
            content = read_pdf_content(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # 데이터셋 청킹하기
        chunks = chunk_text(content)
        
        # 각 청크에 대해 임베딩 생성
        for i, chunk in enumerate(chunks):
            # chroma_client._get_embedding()임베딩하기
            embedding = chroma_client._get_embedding(chunk)
            
            all_documents.append(chunk)
            all_embeddings.append(embedding)
            all_ids.append(f"{dataset_id}_{i}")
    
    # chroma_client.add_documents()로 문서 추가하기
    chroma_client.add_documents(
        collection_name=collection_name,
        documents=all_documents,
        embeddings=all_embeddings,
        ids=all_ids
    )

    print(f"RAG {rag_id} 데이터베이스 구축 완료. {len(all_documents)}개의 문서가 추가되었습니다.")
    return True