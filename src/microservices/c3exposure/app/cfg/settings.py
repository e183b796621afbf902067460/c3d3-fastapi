from pydantic import BaseSettings
from decouple import config


class AppSettings(BaseSettings):

    API_V1: str = config('API_V1', cast=str, default='/api/v1')
    JWT_FERNET_KEY: str = config('JWT_FERNET_KEY', cast=str)
    SERVICE_ENDPOINT: str = config('SERVICE_ENDPOINT', cast=str, default='/c3exposure')

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
