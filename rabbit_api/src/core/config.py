import os
from enum import Enum

from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = 'postgres'
    password: str = 'password'
    host: str = 'localhost'
    port: int = 5432
    db: str = 'movies'

    @property
    def dsn(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'

    class Config:
        env_prefix = "POSTGRES_"


class RabbitMQSettings(BaseSettings):
    user_name: str = 'guest'
    password: str = 'guest'
    host: str = '127.0.0.1'
    port: int = 5672
    exchange: str = ''

    class Config:
        env_prefix = "RABBIT_"


class Settings(BaseSettings):
    uvicorn_reload: bool = True
    project_name: str = 'RabbitService'
    postgres: PostgresSettings = PostgresSettings()
    rabbit: RabbitMQSettings = RabbitMQSettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        use_enum_values = True


settings = Settings()
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Queue(Enum):
    fast = True
    slow = False
