from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
print(f"{BASE_DIR=}")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_PATH: str = str(BASE_DIR / "db.sqlite3")

settings = Settings()