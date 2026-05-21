import httpx
from app.config import settings

SCRAPER_API_URL = "https://api.scraperapi.com"


async def fetch_html(url: str, render_js: bool = True) -> str:
    params = {
        "api_key": settings.scraper_api_key,
        "url": url,
        "render": str(render_js).lower(),
        "country_code": "us",
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(SCRAPER_API_URL, params=params)
        response.raise_for_status()
        return response.text


async def fetch_json(url: str) -> dict:
    params = {
        "api_key": settings.scraper_api_key,
        "url": url,
        "autoparse": "true",
        "country_code": "us",
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(SCRAPER_API_URL, params=params)
        response.raise_for_status()
        return response.json()
