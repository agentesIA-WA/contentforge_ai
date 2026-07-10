"""Environment-driven application settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a .env file."""

    app_name: str = Field(default="Beauty Content AI", validation_alias="APP_NAME")
    environment: str = Field(default="development", validation_alias="APP_ENVIRONMENT")
    debug: bool = Field(default=True, validation_alias="APP_DEBUG")
    api_prefix: str = Field(default="/api/v1", validation_alias="APP_API_PREFIX")
    log_level: str = Field(default="INFO", validation_alias="APP_LOG_LEVEL")

    database_url: str = Field(
        default="postgresql+psycopg://usuario:senha@localhost:5432/beauty_content_ai",
        validation_alias="DATABASE_URL",
    )

    jwt_secret_key: str = Field(
        default="troque-esta-chave-em-producao",
        validation_alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
