from pydantic import BaseSettings, AnyHttpUrl
from decouple import config


class AppSettings(BaseSettings):
    API_V1: str = config('API_V1', cast=str, default='/api/v1')

    C3RESEARCH_SERVICE_ENDPOINT: str = config('C3RESEARCH_SERVICE_ENDPOINT', cast=str, default='/c3research')
    C3EXPOSURE_SERVICE_ENDPOINT: str = config('C3EXPOSURE_SERVICE_ENDPOINT', cast=str, default='/c3exposure')
    D3RESEARCH_SERVICE_ENDPOINT: str = config('D3RESEARCH_SERVICE_ENDPOINT', cast=str, default='/d3research')
    D3EXPOSURE_SERVICE_ENDPOINT: str = config('D3EXPOSURE_SERVICE_ENDPOINT', cast=str, default='/d3exposure')

    AUTH_SERVICE_URL: str = 'http://auth-service:8000'
    C3RESEARCH_SERVICE_URL: str = 'http://c3-research-service:8000'
    C3EXPOSURE_SERVICE_URL: str = 'http://c3-exposure-service:8000'
    D3RESEARCH_SERVICE_URL: str = 'http://d3-research-service:8000'
    D3EXPOSURE_SERVICE_URL: str = 'http://d3-exposure-service:8000'
    WAREHOUSE_URL: str = 'http://warehouse-service:8000'

    JWT_FERNET_KEY: str = config('JWT_FERNET_KEY', cast=str)
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', cast=str, default='HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=60)

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
