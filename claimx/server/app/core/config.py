from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    port: int = 8000
    database_url: str
    jwt_secret: str
    gemini_api_key: str = ""
    frontend_url: str = "http://localhost:5173"
    upload_dir: str = "uploads"
    max_upload_mb: int = 10
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

settings = Settings()
