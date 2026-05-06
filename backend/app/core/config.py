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

    class Config:
        env_file = ".env"


settings = Settings()