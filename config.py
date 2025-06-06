from pydantic import BaseSettings, PostgresDsn
from typing import List, Optional, Dict, Any, Union
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trading Bot"
    PROJECT_DESCRIPTION: str = "A trading bot with backtesting capabilities"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tradingbot")
    SQLALCHEMY_DATABASE_URI: Optional[Union[str, PostgresDsn]] = None
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Build database URI
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()

