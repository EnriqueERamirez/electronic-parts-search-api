from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Electronics Parts API"
    app_version: str = "1.0.0"
    
    digikey_client_id: str = ""
    digikey_client_secret: str = ""
    digikey_api_url: str = "https://api.digikey.com"
    digikey_sandbox_url: str = "https://sandbox-api.digikey.com"
    digikey_use_sandbox: bool = False
    
    mouser_api_key: str = ""
    farnell_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
