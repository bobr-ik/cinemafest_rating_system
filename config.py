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
            "СЦЕНАРИЙ": 0.25,           # 25%
            "АКТЕРСКАЯ ИГРА": 0.25,     # 25%
            "ОПЕРАТОРСКАЯ РАБОТА": 0.15, # 15%
            "МОНТАЖ": 0.15,             # 15%
            "ЗВУКОРЕЖЕССУРА": 0.1,     # 10%
            "ЦЕЛОСТНОСТЬ КАРТИНЫ": 0.1   # 10%
        }

    @property
    def credentials_path(self):
        return ROOT / self.credentials_file_name

    class Config:
        env_file = ROOT / ".env"
        env_file_encoding = "utf-8"
    

settings = Settings()