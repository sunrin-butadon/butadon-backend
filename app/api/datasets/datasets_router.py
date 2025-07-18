from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path

from app.core.config import settings
from app.db.deps import get_db
from app.core.auth import get_current_user
from app.api.datasets import datasets_crud
from app.api.datasets.datasets_dto import DatasetCreateDTO, DatasetResponseDTO
from app.api.datasets.datasets_model import Dataset
from app.api.users import users_crud

router = APIRouter()

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.get("/list", tags=["datasets"], response_model=list[DatasetResponseDTO])
async def list_datasets(db: Session = Depends(get_db)):
    """
    데이터셋 목록을 조회합니다.
    """
    datasets_list = datasets_crud.get_dataset_list(db)
    
    # 각 데이터셋에 대해 username 조회해서 추가
    result = []
    for dataset in datasets_list:
        user = users_crud.get_user_by_id(dataset.made_by_user, db)
        username = user.username if user else "Unknown"
        
        result.append(DatasetResponseDTO(
            id=dataset.id,
            name=dataset.name,
            made_by_user=dataset.made_by_user,
            username=username,
            description=dataset.description,
            file_type=dataset.file_type,
            created_at=dataset.created_at
        ))
    
    return result

@router.get("/{dataset_id}", tags=["datasets"], response_model=DatasetResponseDTO)
async def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = datasets_crud.get_dataset_by_id(dataset_id, db)
    if not dataset:
        raise HTTPException(status_code=404, detail="데이터셋을 찾을 수 없습니다.")
    
    # username 조회
    user = users_crud.get_user_by_id(dataset.made_by_user, db)
    username = user.username if user else "Unknown"
    
    return DatasetResponseDTO(
        id=dataset.id,
        name=dataset.name,
        made_by_user=dataset.made_by_user,
        username=username,
        description=dataset.description,
        file_type=dataset.file_type,
        created_at=dataset.created_at
    )



@router.post("/create", tags=["datasets"], response_model=DatasetResponseDTO)
async def create_dataset(
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    파일을 업로드하고 데이터셋을 생성합니다.
    """
    # 파일 확장자 검증
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"지원되지 않는 파일 형식입니다. 허용된 형식: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="파일 크기가 너무 큽니다. 최대 500MB까지 허용됩니다."
        )
    
    # 고유한 파일 이름 생성
    dataset_id = str(uuid.uuid4())
    file_name = f"{dataset_id}{file_extension}"
    
    file_path = Path(settings.datasets_path) / file_name
    
    try:
        # 파일 저장
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # 데이터베이스에 데이터셋 정보 저장
        dataset_data = DatasetCreateDTO(name=name, description=description)
        dataset = datasets_crud.create_dataset(
            item=dataset_data,
            user_id=current_user["sub"],
            file_type=file_extension[1:],  # . 제거
            db=db
        )
        
        # 파일 이름을 dataset ID로 변경
        new_file_name = f"{dataset.id}{file_extension}"
        new_file_path = Path(settings.datasets_path) / new_file_name
        file_path.rename(new_file_path)
        
        # 사용자의 created_dataset_ids에 추가
        users_crud.add_created_dataset(current_user["sub"], dataset.id, db)
        
        # username 조회
        user = users_crud.get_user_by_id(dataset.made_by_user, db)
        username = user.username if user else "Unknown"
        
        return DatasetResponseDTO(
            id=dataset.id,
            name=dataset.name,
            made_by_user=dataset.made_by_user,
            username=username,
            description=dataset.description,
            file_type=dataset.file_type,
            created_at=dataset.created_at
        )
        
    except Exception as e:
        # 파일 저장 실패 시 파일 삭제
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"파일 저장 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/{dataset_id}/download", tags=["datasets"])
async def download_dataset_file(
    dataset_id: str,
    db: Session = Depends(get_db)):
    """
    데이터셋 파일을 다운로드합니다.
    """
    from fastapi.responses import FileResponse
    
    dataset = datasets_crud.get_dataset_by_id(dataset_id, db)

    if not dataset:
        raise HTTPException(status_code=404, detail="데이터셋을 찾을 수 없습니다.")
    
    # 파일 경로 생성 (dataset ID를 파일명으로 사용)
    upload_dir = Path(settings.datasets_path)
    file_path = upload_dir / f"{dataset.id}.{dataset.file_type}"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    return FileResponse(
        path=str(file_path),
        filename=f"{dataset.name}.{dataset.file_type}",
        media_type="application/octet-stream"
    )
