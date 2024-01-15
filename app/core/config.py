import os
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    BASE_URL: str = os.environ.get('BASE_URL', '')

    DB_NAME: str = os.environ.get('DB_NAME', 'billing')
    DB_USER: str = os.environ.get('DB_USER', 'acre_service')
    DB_HOST: str = os.environ.get('DB_HOST', '172.21.0.2')
    DB_PORT: str = os.environ.get('DB_PORT', '5433')
    DB_PW: str = os.environ.get('DB_PW', '')

    SQLALCHEMY_DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    db_echo: bool = True
    API_KEY: str = os.environ.get('API_KEY', '')

config = Config()
