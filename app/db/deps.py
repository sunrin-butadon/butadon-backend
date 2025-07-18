from app.db.sqlite.database import SessionLocal
from app.db.chroma.client import chroma_client

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_chroma_client():
    return chroma_client