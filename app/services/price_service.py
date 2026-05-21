import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, PriceRecord
from app.schemas.product import PriceResult, PriceHistoryResult, PriceHistoryItem
from app.cache import cache_get, cache_set
from app.scrapers import amazon

SCRAPERS = {
    "amazon": amazon.scrape,
}


async def get_price(product_id: str, source: str, db: AsyncSession) -> PriceResult:
    cache_key = f"price:{source}:{product_id}"
    cached = await cache_get(cache_key)
    if cached:
        result = PriceResult(**cached)
        result.cached = True
        return result

    scraper = SCRAPERS[source]
    result = await scraper(product_id)

    await _persist(result, db)
    await cache_set(cache_key, result.model_dump(mode="json"))

    return result


async def search_prices(query: str, sources: list[str], db: AsyncSession) -> list[PriceResult]:
    # Parallel scrape across requested sources using query as product_id
    # For MVP: query is treated as product_id per source
    tasks = [get_price(query, source, db) for source in sources if source in SCRAPERS]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, PriceResult)]


async def get_history(product_id: str, source: str, days: int, db: AsyncSession) -> PriceHistoryResult:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stmt = (
        select(Product)
        .where(Product.product_id == product_id, Product.source == source)
        .options(selectinload(Product.prices))
    )
    product = (await db.execute(stmt)).scalar_one_or_none()

    if not product:
        return PriceHistoryResult(product_id=product_id, source=source, title=None, history=[])

    records = [r for r in product.prices if r.scraped_at.replace(tzinfo=timezone.utc) >= cutoff]

    return PriceHistoryResult(
        product_id=product_id,
        source=source,
        title=product.title,
        history=[
            PriceHistoryItem(
                price=r.price,
                currency=r.currency,
                availability=r.availability,
                scraped_at=r.scraped_at,
            )
            for r in records
        ],
    )


async def _persist(result: PriceResult, db: AsyncSession) -> None:
    stmt = select(Product).where(
        Product.product_id == result.product_id,
        Product.source == result.source,
    )
    product = (await db.execute(stmt)).scalar_one_or_none()

    if not product:
        product = Product(
            product_id=result.product_id,
            source=result.source,
            title=result.title,
        )
        db.add(product)
        await db.flush()

    db.add(PriceRecord(
        product_id=product.id,
        price=result.price,
        currency=result.currency,
        availability=result.availability,
    ))
    await db.commit()
