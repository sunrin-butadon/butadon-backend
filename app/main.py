from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers import router
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    if not os.path.exists(settings.database_path):
        from app.db.sqlite.init_db import init_db
        init_db()
    
    from app.db.chroma.client import chroma_client
    chroma_client.get_or_create_collection(
        "default_collection", 
        metadata={"description": "Default collection for the application"}
    )
    print(chroma_client.collections)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}   