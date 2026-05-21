from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import prices
import app.models.product  # ensure models are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="PriceRadar API",
    description="Real-time e-commerce price data from Amazon and Walmart",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(prices.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
