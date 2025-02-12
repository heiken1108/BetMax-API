from fastapi import FastAPI
from app.api.routes import router
from contextlib import asynccontextmanager
import aiohttp
from datetime import date
import pandas as pd
import io
from app.background.data_updater import DataUpdater

data_updater = DataUpdater()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown tasks."""
    await data_updater.start()
    yield  # Keep the app running
    print("Server is shutting down...")

app = FastAPI(title="Bet Maximizer API", lifespan=lifespan)

app.include_router(router)