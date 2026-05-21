import re
from datetime import datetime, timezone
from app.scrapers.base import fetch_json
from app.schemas.product import PriceResult


def _parse_price(raw: str | None) -> float | None:
    if not raw:
        return None
    cleaned = re.sub(r"[^\d.]", "", raw.replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return None


async def scrape(asin: str) -> PriceResult:
    url = f"https://www.amazon.com/dp/{asin}"
    data = await fetch_json(url)

    return PriceResult(
        product_id=asin,
        source="amazon",
        title=data.get("name"),
        price=_parse_price(data.get("pricing")),
        currency="USD",
        availability=data.get("availability_status"),
        scraped_at=datetime.now(timezone.utc),
    )
