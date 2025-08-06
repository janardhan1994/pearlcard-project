# backend/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Defines application settings, reading from a .env file or environment variables.
    """
    # Define your configuration variables with types and default values
    DATABASE_URL: str = "sqlite+aiosqlite:///../pearlcard.db"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    # This tells Pydantic to look for a .env file in this directory
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Create a single, importable instance of the settings
settings = Settings()