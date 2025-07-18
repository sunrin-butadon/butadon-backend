import chromadb
from chromadb.errors import NotFoundError
from app.core.config import settings
from openai import OpenAI

class ChromaDBClient:
    def __init__(self):
        # ChromaDB 클라이언트 생성 (영구 저장을 위해 파일 시스템 사용)
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.openai_client = OpenAI(api_key=settings.openai_api_key)

    def _get_embedding(self, text: str) -> list:
        embedding = self.openai_client.embeddings.create(
            input=text,
            model=settings.openai_embeddings_model
        )
        return embedding.data[0].embedding

    def get_chroma_collection_name(self, rag_id: str) -> str:
        # rag_id에서 하이픈을 언더스코어로 변경하여 컬렉션 이름 반환
        return f"rag_{rag_id.replace('-', '_')}"
    
    def create_or_get_collection(self, collection_name: str):
        # 컬렉션 생성 (이미 있으면 가져옴)
        try:
            collection = self.client.get_collection(collection_name)
        except NotFoundError:
            collection = self.client.create_collection(name=collection_name)
        return collection

    def add_documents(self, collection_name: str, documents: list, embeddings: list, ids: list):
        # 컬렉션에 문서와 임베딩을 저장
        collection = self.create_or_get_collection(collection_name)
        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )

    def search_by_embedding(self, collection_name: str, query_embedding: list, n_results: int = 5):
        # 임베딩 벡터로 문서 검색
        collection = self.create_or_get_collection(collection_name)
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results
    
chroma_client = ChromaDBClient()