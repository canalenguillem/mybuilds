"""Application configuration loaded from environment variables."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings object. Values come from the environment / .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    app_name: str = "myBuilds Submittal Automation System"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"

    # Databases / cache
    database_url: str = "mysql+pymysql://submittal_user:password@mariadb:3306/submittal_db"
    mongodb_url: str = "mongodb://admin:password@mongodb:27017/submittal_db?authSource=admin"
    mongodb_database: str = "submittal_db"
    redis_url: str = "redis://:password@redis:6379/0"

    # Celery
    celery_broker_url: str = "redis://:password@redis:6379/1"
    celery_result_backend: str = "redis://:password@redis:6379/2"

    # JWT
    jwt_secret_key: str = "dev-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # AI / LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_timeout: int = 60
    anthropic_api_key: str = ""
    llm_model: str = "claude-opus-4-8"

    # Security
    cors_origins: str = "http://localhost:3000,http://localhost"
    allowed_hosts: str = "localhost,127.0.0.1"

    # File storage
    file_storage_type: str = "local"
    file_max_size_mb: int = 50
    allowed_file_types: str = "pdf"
    documents_path: str = "/app/data/documents"
    generated_pdfs_path: str = "/app/data/generated_pdfs"

    # Seed admin
    seed_admin_email: str = "admin@mybuilds.com"
    seed_admin_username: str = "admin"
    seed_admin_password: str = "Admin123!"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def allowed_file_types_list(self) -> list[str]:
        return [t.strip().lower() for t in self.allowed_file_types.split(",") if t.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor used throughout the app."""
    return Settings()


settings = get_settings()
