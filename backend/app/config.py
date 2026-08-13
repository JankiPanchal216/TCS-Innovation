import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PGHOST: str = "localhost"
    PGPORT: int = 5432
    PGUSER: str = "postgres"
    PGPASSWORD: str = "postgres"
    PGDATABASE: str = "libraai"
    
    # Base configuration for reading from .env file
    # Look for .env in the backend folder or database folder
    model_config = SettingsConfigDict(env_file=["../database/.env", ".env"], env_file_encoding="utf-8", extra="ignore")
    
    # Ollama Embeddings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_EMBEDDING_MODEL: str = "qwen3-embedding"
    OLLAMA_EMBEDDING_TIMEOUT_SECONDS: int = 60
    OLLAMA_EMBEDDING_BATCH_SIZE: int = 16
    OLLAMA_MAX_RETRIES: int = 3
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

settings = Settings()
