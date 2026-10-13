from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "notification-service"
    port: int = 8084
    host_name: str = "localhost"
    ip_addr: str = "127.0.0.1"

    eureka_url: str = "http://localhost:8761/eureka"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "notifications_db"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
