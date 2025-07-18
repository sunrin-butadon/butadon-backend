from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import TEXT
import uuid
from app.db.sqlite.base import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    made_by_user = Column(String, nullable=False)  # User CUID
    description = Column(String, nullable=True)
    file_type = Column(String, nullable=False)  # e.g., 'pdf', 'txt' 
    created_at = Column(String, nullable=False)  # Store as ISO format string