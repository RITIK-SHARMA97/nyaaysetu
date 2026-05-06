from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    GEMINI_API_KEY: str = "placeholder"
    GEMINI_MODEL: str = "gemini-flash-latest"
    DATABASE_URL: str = "postgresql://nyaay:setu2024@db:5432/nyaaysetu"
    JWT_SECRET: str = "nyaaysetu-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480
    MAX_PDF_MB: int = 50
    TESSERACT_LANG: str = "eng"
    UPLOAD_DIR: str = "uploads"
    ESCALATION_CRITICAL_DAYS: int = 7
    ESCALATION_URGENT_DAYS: int = 15
    ESCALATION_WARNING_DAYS: int = 30

settings = Settings()
