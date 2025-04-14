
from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Defines application settings using Pydantic for environment-based configuration.

Includes OpenSearch connection parameters and host/port setup for the API server.
"""


class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8080

    opensearch_host: str
    opensearch_user: str
    opensearch_password: str

    model_config = SettingsConfigDict(env_file = '.env')
    
settings = Settings()