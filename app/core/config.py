from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DSN: str = "mongodb://localhost:27017"
    MONGO_DB: str = "ai_todo"
    JWT_SECRET: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"


settings = Settings()
