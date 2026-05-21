from datetime import datetime
from pydantic import BaseModel


class PriceResult(BaseModel):
    product_id: str
    source: str
    title: str | None
    price: float | None
    currency: str
    availability: str | None
    cached: bool = False
    scraped_at: datetime


class PriceHistoryItem(BaseModel):
    price: float | None
    currency: str
    availability: str | None
    scraped_at: datetime


class PriceHistoryResult(BaseModel):
    product_id: str
    source: str
    title: str | None
    history: list[PriceHistoryItem]


class SearchResult(BaseModel):
    results: list[PriceResult]
