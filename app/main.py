from fastapi import FastAPI
from app.api.routes import router
from contextlib import asynccontextmanager
import aiohttp
from datetime import date
import pandas as pd
import io

CSV_URL = f"http://api.clubelo.com/{date.today().isoformat()}"
LOCAL_CSV_PATH = "app/files/elo_ratings.csv"
FIXTURES_URL = f"http://api.clubelo.com/Fixtures"
LOCAL_FIXTURES_CSV_PATH = "app/files/fixtures.csv"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown tasks."""
    await download_elo_csv()
    await download_fixtures_predictions_csv()
    yield  # Keep the app running
    print("Server is shutting down...")
    
async def download_elo_csv():
    async with aiohttp.ClientSession() as session:
        async with session.get(CSV_URL) as response:
            if response.status == 200:
                csv_data = await response.text()
                df = pd.read_csv(io.StringIO(csv_data))
                df.set_index('Club', inplace=True)
                df.to_csv(LOCAL_CSV_PATH)
                print(f"CSV downloaded and saved to {LOCAL_CSV_PATH}")
            else:
                print(f"Failed to fetch CSV: {response.status}")

async def download_fixtures_predictions_csv():
    async with aiohttp.ClientSession() as session:
        async with session.get(FIXTURES_URL) as response:
            if response.status == 200:
                csv_data = await response.text()
                df = pd.read_csv(io.StringIO(csv_data), index_col=['Home', 'Away'])
                df.to_csv(LOCAL_FIXTURES_CSV_PATH)
                print(f"CSV downloaded and saved to {LOCAL_FIXTURES_CSV_PATH}")
            else:
                print(f"Failed to fetch CSV: {response.status}")

app = FastAPI(title="Bet Maximizer API", lifespan=lifespan)

app.include_router(router)