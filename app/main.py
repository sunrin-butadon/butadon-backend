from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.core.config import settings
from app.api.routers import router
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

    # 데이터셋 저장 디렉토리 설정
    Path(settings.datasets_path).mkdir(parents=True, exist_ok=True)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}   