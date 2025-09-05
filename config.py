from pydantic_settings import BaseSettings
import pathlib


ROOT = pathlib.Path(__file__).parent


class Settings(BaseSettings):
    credentials_file_name: str
    table_url: str
    worksheet_name: str

    @property
    def criteria_weights(self) -> dict:
        return {
            "СЦЕНАРИЙ": 4,
            "АКТЕРСКАЯ ИГРА": 4,
            "ЦЕЛОСТНОСТЬ КАРТИНЫ": 4,
            "МОНТАЖ": 3,
            "ЗВУКОРЕЖЕССУРА": 3,
            "ОПЕРАТОРСКАЯ РАБОТА": 3,
        }

    @property
    def credentials_path(self):
        return ROOT / self.credentials_file_name

    class Config:
        env_file = ROOT / ".env"
        env_file_encoding = "utf-8"
    

settings = Settings()