
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8080

    opensearch_host: str
    opensearch_user: str
    opensearch_password: str

    model_config = SettingsConfigDict(env_file = '.env')
    
settings = Settings()