from sqlalchemy import (Column,
                        String)
import cuid

from app.db.sqlite.base import Base

class User(Base):
    __tablename__ = "users"

    cuid = Column(String, primary_key=True, index=True, default=cuid.cuid)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    bookmarked_rag_ids = Column(String, default="[]")  # Store as JSON string
    bookmarked_dataset_ids = Column(String, default="[]")  # Store as JSON string

    created_rag_ids = Column(String, default="[]")  # Store as JSON string
    created_dataset_ids = Column(String, default="[]")  # Store as JSON string