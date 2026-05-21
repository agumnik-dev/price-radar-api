from datetime import datetime, timezone
from bs4 import BeautifulSoup
from app.scrapers.base import fetch_html
from app.schemas.product import PriceResult


def _build_url(product_id: str) -> str:
    return f"https://www.walmart.com/ip/{product_id}"


def _parse_price(soup: BeautifulSoup) -> float | None:
    for selector in ["[itemprop='price']", "[data-automation='product-price']", ".price-characteristic"]:
        el = soup.select_one(selector)
        if el:
            raw = el.get("content") or el.get_text()
            text = raw.strip().replace("$", "").replace(",", "")
            try:
                return float(text)
            except ValueError:
                continue
    return None


def _parse_title(soup: BeautifulSoup) -> str | None:
    for selector in ["[itemprop='name']", "h1.prod-ProductTitle", "h1"]:
        el = soup.select_one(selector)
        if el:
            return el.get_text().strip()
    return None


def _parse_availability(soup: BeautifulSoup) -> str | None:
    el = soup.select_one("[data-automation='add-to-cart-section']")
    return el.get_text().strip() if el else None


async def scrape(product_id: str) -> PriceResult:
    url = _build_url(product_id)
    html = await fetch_html(url, render_js=True)
    soup = BeautifulSoup(html, "lxml")

    return PriceResult(
        product_id=product_id,
        source="walmart",
        title=_parse_title(soup),
        price=_parse_price(soup),
        currency="USD",
        availability=_parse_availability(soup),
        scraped_at=datetime.now(timezone.utc),
    )
