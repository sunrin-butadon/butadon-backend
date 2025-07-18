from app.db.sqlite.base import Base
from app.db.sqlite.database import engine 

def init_db():
    Base.metadata.create_all(bind=engine)