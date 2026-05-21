from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379"
    scraper_api_key: str
    cache_ttl: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
