from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mysql_database: str
    mysql_user: str
    mysql_password: str
    mysql_host: str = "mysql"
    mysql_port: int = 3306

    mongodb_host: str = "mongodb"
    mongodb_port: int = 27017
    mongodb_database: str = "event_ticketing"

    redis_host: str = "redis"
    redis_port: int = 6379

    event_cache_ttl_seconds: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    @property
    def mysql_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    @property
    def mongodb_url(self) -> str:
        return (
            f"mongodb://{self.mongodb_host}:"
            f"{self.mongodb_port}/"
        )


settings = Settings()