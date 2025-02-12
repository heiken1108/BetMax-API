from pydantic_settings import BaseSettings
from datetime import date


class Settings(BaseSettings):
    ELO_URL = f"http://api.clubelo.com/{date.today().isoformat()}"
    FIXTURES_URL = "http://api.clubelo.com/Fixtures"
    ELO_CSV_PATH = "app/files/elo_ratings.csv"
    FIXTURES_CSV_PATH = "app/files/fixtures.csv"
    UPDATE_INTERVAL = 60

    class Config:
        env_file = ".env"

settings = Settings()