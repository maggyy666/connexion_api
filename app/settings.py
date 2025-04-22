
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

"""
Defines application settings using Pydantic for environment-based configuration.

Includes OpenSearch connection parameters and host/port setup for the API server.
"""


class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = Field(default="127.0.01", validation_alias="HOST")
    PORT: int = Field(default=8080, validation_alias="PORT")

    opensearch_host: str = Field(... , validation_alias="OPENSEARCH_HOST")
    opensearch_user: str = Field(... , validation_alias="OPENSEARCH_USER")
    opensearch_password: str = Field(... , validation_alias="OPENSEARCH_PASSWORD")


    model_config = SettingsConfigDict(env_file = '.env')
    
settings = Settings()