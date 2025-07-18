from pydantic import BaseModel, Field, computed_field


class DatasetCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=3000)

class DatasetResponseDTO(BaseModel):
    id: str
    name: str
    made_by_user: str  # User CUID
    description: str | None = None
    file_type: str  # e.g., 'pdf', 'txt'
    created_at: str  # ISO format string for created_at
    
    @computed_field
    @property
    def filename(self) -> str:
        """데이터셋 이름과 확장자를 포함한 전체 파일명"""
        return f"{self.name}.{self.file_type}"
    
    @computed_field
    @property
    def download_url(self) -> str:
        """파일 다운로드 URL"""
        return f"/api/datasets/{self.id}/download"
