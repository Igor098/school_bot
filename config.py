import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath((os.path.dirname(__file__)))
    DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/db.sqlite3"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


# Получаем параметры для загрузки переменных среды
settings = Settings()
database_url = settings.DB_URL
database_dir = settings.BASE_DIR
