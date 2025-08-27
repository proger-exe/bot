from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""
    bot_token: str
    postgres_dsn: str

    class Config:
        env_file = ".env"

settings = Settings()
