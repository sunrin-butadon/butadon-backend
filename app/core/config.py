from pydantic_settings import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    app_name: str

    # SQL Database settings
    database_path: str
    database_url: str
    
    # Chroma DB settings
    chroma_db_path: str

    # JWT settings
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    # OpenAI API settings
    openai_api_key: str
    openai_embeddings_model: str

    # File upload settings
    datasets_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

load_dotenv()
settings = Settings()

print(settings)