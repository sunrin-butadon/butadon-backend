import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.errors import NotFoundError, InvalidArgumentError
from typing import List, Dict, Optional
import os
from app.core.config import settings

class ChromaDBClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            settings=ChromaSettings(
                allow_reset=True,
                anonymized_telemetry=False
            )
        )
        self.collections:list[str] = self.client.list_collections()
        
    def get_or_create_collection(self, name: str, metadata: Optional[Dict] = None):
        """컬렉션을 가져오거나 생성"""
        try:
            return self.client.get_collection(name=name)
        except NotFoundError:
            # 메타데이터가 비어있으면 None으로 설정
            collection_metadata = metadata if metadata else None
            return self.client.create_collection(
                name=name,
                metadata=collection_metadata
            )
        except Exception as e:
            print(f"Error in get_or_create_collection: {e}")
            raise
    
    def add_documents(self, 
                     collection_name: str, 
                     documents: List[str], 
                     metadatas: Optional[List[Dict]] = None,
                     ids: Optional[List[str]] = None):
        """문서들을 컬렉션에 추가"""
        collection = self.get_or_create_collection(collection_name)
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
            
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_documents(self, 
                        collection_name: str, 
                        query: str, 
                        n_results: int = 10,
                        where: Optional[Dict] = None):
        """문서 검색"""
        collection = self.get_or_create_collection(collection_name)
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )
        
        return results
    
    def delete_collection(self, collection_name: str):
        """컬렉션 삭제"""
        try:
            self.client.delete_collection(name=collection_name)
        except Exception as e:
            print(f"Error deleting collection {collection_name}: {e}")



chroma_client = ChromaDBClient()
