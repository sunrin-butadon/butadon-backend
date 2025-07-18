from pydantic import BaseModel, Field, computed_field


class DatasetCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=3000)

class DatasetResponseDTO(BaseModel):
    id: str = Field(example="90c76ad8-e7b2-4d8b-8651-64801fbd9939")
    name: str = Field(example="보고서")
    made_by_user: str = Field(example="cmd8ts5lc0000y03qs7la34qp")  # User CUID
    description: str | None = Field(None, example="string")
    file_type: str = Field(example="pdf")  # e.g., 'pdf', 'txt'
    created_at: str = Field(example="2025-07-18T21:59:31.467627")  # ISO format string for created_at
    
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
