from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_NAME: str
    BASE_DIR: Path = Path(__file__).resolve().parents[1]



    @computed_field
    @property
    def database_url(self) -> str:
        return   f"sqlite+aiosqlite:///{str(self.BASE_DIR / self.DATABASE_NAME)}"

settings = Settings()