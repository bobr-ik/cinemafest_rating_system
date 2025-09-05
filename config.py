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
            "АКТЕРСКАЯ ИГРА": 0.20,     # 20%
            "ОПЕРАТОРСКАЯ РАБОТА": 0.20, # 20%
            "МОНТАЖ": 0.15,             # 15%
            "ЗВУКОРЕЖЕССУРА": 0.15,     # 15%
            "ЦЕЛОСТНОСТЬ КАРТИНЫ": 0.05   # 5%
        }

    @property
    def credentials_path(self):
        return ROOT / self.credentials_file_name

    class Config:
        env_file = ROOT / ".env"
        env_file_encoding = "utf-8"
    

settings = Settings()