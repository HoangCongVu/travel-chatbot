from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "local"  # local | dev | prod
    DEBUG: bool = True
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    class Config:
        env_file = ".env"
        extra = "ignore"  # Cho phép bỏ qua key thừa trong .env (nếu có)
        

env = Settings()
