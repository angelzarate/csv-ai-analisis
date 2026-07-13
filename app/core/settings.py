from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

class AppSettings(BaseSettings):
    # Add your settings here
    app_name: str = "My Application"
    app_version: str = "1.0.0"
    debug: bool = True    

    #
    max_workers: int = 8


    # db
    db_connection: str = ""


    # openai vars
    ai_endpoint: str = "https://api.openai.com/v1"
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 1024


    storage_dir: Path = Field(default=Path("storage"))



    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> AppSettings:
    Path("storage").mkdir(exist_ok=True)
    return AppSettings()