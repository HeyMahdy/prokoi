from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Local DB (old)
    # DB_HOST: str = "localhost"
    # DB_PORT: int = 3306
    # DB_USER: str = "root"
    # DB_PASSWORD: str = ""
    # DB_NAME: str = "prokoi"

    # Production DB (Neon)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
