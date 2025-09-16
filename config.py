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
            "СЦЕНАРИЙ": 0.2,           # 20%
            "АКТЕРСКАЯ ИГРА": 0.2,     # 20%
            "ЗРЕЛИЩНОСТЬ": 0.15,       # 15%
            "МОНТАЖ": 0.13,             # 13%
            "ОПЕРАТОРСКАЯ РАБОТА": 0.13, # 13%
            "ЗВУКОРЕЖЕССУРА": 0.13,     # 13%
            "ЦЕЛОСТНОСТЬ КАРТИНЫ": 0.06   # 6%
        }

    @property
    def credentials_path(self):
        return ROOT / self.credentials_file_name

    class Config:
        env_file = ROOT / ".env"
        env_file_encoding = "utf-8"
    

settings = Settings()