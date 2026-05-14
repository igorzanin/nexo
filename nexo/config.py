from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nexo.db"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_days: int = 30
    refresh_token_expire_days: int = 60
    enable_public_shared_boards: bool = False
    max_file_size: int = 102400
    rate_limit_per_minute: int = 60
    server_root: str = "http://localhost:8000"
    port: int = 8000
    local_only: bool = False
    ssl_enabled: bool = False
    read_header_timeout: int = 10


@lru_cache
def get_settings() -> Settings:
    return Settings()
