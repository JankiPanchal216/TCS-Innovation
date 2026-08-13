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
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

settings = Settings()
