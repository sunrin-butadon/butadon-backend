from sqlalchemy import Column, String, Integer

from app.db.sqlite.base import Base

class RagModel(Base):
    __tablename__ = "rags"

    id = Column(String, primary_key=True, index=True) # UUID

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    made_by_user = Column(String, nullable=False)  # User CUID
    created_at = Column(String, nullable=False)  # Store as ISO format string

    dataset_ids = Column(String, nullable=False, default="[]")  # JSON string of dataset IDs
    llm_model = Column(String, nullable=False)  # OpenAI model name
    chunk_size = Column(Integer, nullable=False)  # Chunk size for text processing
    