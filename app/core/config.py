from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

class Settings(BaseSettings):
    app_name: str = "AI Portfolio Tracker"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./portfolio.db"
    twelve_data_api_key: str | list[str] = Field(default_factory=list)

    @field_validator("twelve_data_api_key", mode="before")
    @classmethod
    def parse_keys(cls, v):
        if isinstance(v, str):
            return [k.strip() for k in v.split(",") if k.strip()]
        return v
    model_config = SettingsConfigDict(env_file =".env", env_file_encoding = "utf-8")


settings = Settings()