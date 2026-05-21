from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import PriceResult, PriceHistoryResult, SearchResult
from app.services import price_service

router = APIRouter(prefix="/api/v1", tags=["prices"])

VALID_SOURCES = {"amazon"}
COMING_SOON_SOURCES = {"walmart", "bestbuy", "ebay"}


@router.get("/price", response_model=PriceResult)
async def get_price(
    product_id: str = Query(..., description="Amazon ASIN (e.g. B09C27LNBS)"),
    source: str = Query(..., description="Supported: amazon. Coming soon: walmart, bestbuy, ebay"),
    db: AsyncSession = Depends(get_db),
):
    if source in COMING_SOON_SOURCES:
        raise HTTPException(status_code=422, detail=f"'{source}' support is coming soon. Currently supported: {sorted(VALID_SOURCES)}")
    if source not in VALID_SOURCES:
        raise HTTPException(status_code=400, detail=f"Unknown source. Supported: {sorted(VALID_SOURCES)}")
    return await price_service.get_price(product_id, source, db)


@router.get("/prices", response_model=SearchResult)
async def search_prices(
    query: str = Query(..., description="Product ID to look up across sources"),
    sources: str = Query(default="amazon", description="Comma-separated sources (amazon)"),
    db: AsyncSession = Depends(get_db),
):
    source_list = [s.strip() for s in sources.split(",") if s.strip() in VALID_SOURCES]
    if not source_list:
        raise HTTPException(status_code=400, detail=f"No valid sources. Supported: {sorted(VALID_SOURCES)}")
    results = await price_service.search_prices(query, source_list, db)
    return SearchResult(results=results)


@router.get("/history", response_model=PriceHistoryResult)
async def get_history(
    product_id: str = Query(..., description="Amazon ASIN"),
    source: str = Query(..., description="Supported: amazon"),
    days: int = Query(default=30, ge=1, le=90),
    db: AsyncSession = Depends(get_db),
):
    if source not in VALID_SOURCES:
        raise HTTPException(status_code=400, detail=f"source must be one of {sorted(VALID_SOURCES)}")
    return await price_service.get_history(product_id, source, days, db)
