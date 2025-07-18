from sqlalchemy import (Column,
                        String)
from sqlalchemy.orm import relationship
import cuid

from app.db.sqlite.base import Base

class User(Base):
    __tablename__ = "users"

    cuid = Column(String, primary_key=True, index=True, default=cuid.cuid)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)