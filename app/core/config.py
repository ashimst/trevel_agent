import os
if "SSL_CERT_FILE" in os.environ and not os.path.exists(os.environ["SSL_CERT_FILE"]):
    del os.environ["SSL_CERT_FILE"]

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "travels_db"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI Agent LLM keys
    GROQ_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    NVIDIA_API_KEY: str = ""
    EXA_API_KEY: str = ""

    # Agent config
    AGENT_MAX_ITERATIONS: int = 15
    CHECKPOINT_DB_NAME: str = "travels_checkpoints"


settings = Settings()
