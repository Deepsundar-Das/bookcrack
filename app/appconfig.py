from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_PORT: int
    REDIS_HOST: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


appConfig = AppConfig()
