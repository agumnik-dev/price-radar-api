# PriceRadar — Technical Architecture

## Overview
A Python/FastAPI REST API that scrapes Amazon product prices via ScraperAPI,
caches results in Redis, persists price history in PostgreSQL, and serves
structured JSON responses.

## System Diagram
```
Client (RapidAPI) → FastAPI → Redis Cache
                           ↓ (cache miss)
                       ScraperAPI → Amazon.com
                           ↓
                       PostgreSQL (price history)
```

## Stack
| Layer       | Technology              | Purpose                          |
|-------------|-------------------------|----------------------------------|
| API         | FastAPI + Uvicorn       | Async REST endpoints             |
| Scraping    | ScraperAPI (autoparse)  | Fetch + parse Amazon pages       |
| Cache       | Redis                   | 1hr TTL cache, avoid re-scraping |
| Database    | PostgreSQL + SQLAlchemy | Store price history              |
| Hosting     | Railway                 | API + Postgres + Redis           |
| Marketplace | RapidAPI                | Billing, metering, distribution  |

## Project Structure
```
price-radar-api/
├── app/
│   ├── main.py                 # FastAPI app, lifespan, router registration
│   ├── config.py               # Settings from .env (pydantic-settings)
│   ├── database.py             # Async SQLAlchemy engine + session
│   ├── cache.py                # Redis get/set helpers
│   ├── models/
│   │   └── product.py          # Product + PriceRecord ORM models
│   ├── schemas/
│   │   └── product.py          # Pydantic response schemas
│   ├── routers/
│   │   └── prices.py           # API endpoints (/price, /prices, /history)
│   ├── scrapers/
│   │   ├── base.py             # ScraperAPI fetch wrapper (fetch_html, fetch_json)
│   │   ├── amazon.py           # Amazon scraper using autoparse=true
│   │   └── walmart.py          # Walmart stub (blocked, not in use)
│   └── services/
│       └── price_service.py    # Business logic, cache + DB orchestration
├── Dockerfile                  # Python 3.12-slim, dynamic PORT
├── docker-compose.yml          # Local dev: API + Postgres + Redis
├── requirements.txt
└── openapi.json                # Auto-generated OpenAPI spec with servers URL
```

## Key Design Decisions

### ScraperAPI autoparse=true
Instead of parsing raw HTML with CSS selectors (fragile, breaks when Amazon
changes layout), we use ScraperAPI's autoparse mode which returns structured
JSON directly. Amazon layout changes are ScraperAPI's problem, not ours.

### Caching Strategy
All price results are cached in Redis with a 1hr TTL.
Cache key: `price:{source}:{product_id}`
This reduces ScraperAPI usage by ~80% for repeated ASIN lookups.

### Price History
Every scrape result is persisted to PostgreSQL regardless of cache state.
The `/history` endpoint returns up to 90 days of price records from the DB.
Useful for trend analysis and price drop detection.

### Async Throughout
FastAPI + async SQLAlchemy + async Redis + httpx — fully async stack.
No blocking I/O. Important for handling concurrent RapidAPI requests.

## Database Schema
```sql
products (
  id            SERIAL PRIMARY KEY,
  product_id    VARCHAR NOT NULL,   -- Amazon ASIN
  source        VARCHAR NOT NULL,   -- 'amazon'
  title         VARCHAR,
  url           VARCHAR,
  created_at    TIMESTAMP,
  UNIQUE(product_id, source)
)

price_records (
  id            SERIAL PRIMARY KEY,
  product_id    INTEGER REFERENCES products(id),
  price         FLOAT,
  currency      VARCHAR DEFAULT 'USD',
  availability  VARCHAR,
  scraped_at    TIMESTAMP
)
```

## API Endpoints
| Method | Path              | Description                        |
|--------|-------------------|------------------------------------|
| GET    | /health           | Health check                       |
| GET    | /api/v1/price     | Current price by ASIN + source     |
| GET    | /api/v1/prices    | Multi-source price lookup          |
| GET    | /api/v1/history   | Price history (1-90 days)          |

## Environment Variables
| Variable         | Description                        |
|------------------|------------------------------------|
| DATABASE_URL     | PostgreSQL async connection string |
| REDIS_URL        | Redis connection string            |
| SCRAPER_API_KEY  | ScraperAPI account key             |
| CACHE_TTL        | Redis TTL in seconds (default 3600)|

## Deployment
- **Local:** `docker compose up` — spins up API + Postgres + Redis
- **Production:** Railway — auto-deploys from `railway up`, PORT injected dynamically
- **Public URL:** https://api-production-73a9.up.railway.app

## Known Limitations
- Walmart returns 403 even with residential proxies — not supported
- Amazon products showing "See All Buying Options" return price=null
  (Apple, Nike and similar brand-controlled listings)
- ScraperAPI free tier: 5,000 requests/month — upgrade needed at scale
