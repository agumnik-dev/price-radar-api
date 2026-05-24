from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from app.database import engine, Base
from app.routers import prices
from app.scrapers import amazon
import app.models.product  # ensure models are registered

# Known stable ASIN used for health checks
HEALTH_CHECK_ASIN = "B09C27LNBS"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="PriceRadar API",
    description="Real-time Amazon product prices, availability, and 90-day price history.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(prices.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/deep")
async def health_deep(response: Response):
    try:
        result = await amazon.scrape(HEALTH_CHECK_ASIN)
        if result.title is None:
            response.status_code = 503
            return {"status": "degraded", "reason": "scraper returned no title"}
        return {
            "status": "ok",
            "asin": HEALTH_CHECK_ASIN,
            "title": result.title,
            "price": result.price,
        }
    except Exception as e:
        response.status_code = 503
        return {"status": "error", "reason": str(e)}
