from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str

    DB_PATH: str

    ARTIFACTS_DIR: str
    MODELS_DIR: str
    LOGS_DIR: str

    API_HOST: str
    API_PORT: int

    DEBUG: bool = True
    
    GOOGLE_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    GEMINI_TEMPERATURE: float = 0.2

    class Config:
        env_file = ".env"


settings = Settings()