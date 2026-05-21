# PriceRadar API

## Idea
A REST API that scrapes and returns real-time product prices from major e-commerce retailers (Amazon, Walmart, eBay, BestBuy). Sold as a subscription on RapidAPI marketplace — no marketing needed, distribution is built-in.

Target customers: small retailers, dropshippers, price comparison sites, and any business needing competitor price intelligence.

## Goal
Generate passive income via RapidAPI with zero active marketing. Reach $300–500/month MRR within 3 months of launch.

## Tech Stack
- **Scraping:** Python + Playwright (handles JS-heavy pages, bypasses basic bot detection)
- **API layer:** FastAPI (fast, async, auto-generates docs)
- **Storage:** PostgreSQL (price history) + Redis (caching, rate limiting)
- **Hosting:** Railway or Fly.io (simple deploy, free tier to start)
- **Billing/distribution:** RapidAPI (handles payments, metering, discovery)

## MVP Scope (Phase 1)

### Endpoints
- `GET /price?asin={id}&source=amazon` — single product price
- `GET /prices?query={term}&sources=amazon,walmart` — search across retailers
- `GET /history?asin={id}&days=30` — price history

### Retailers (start with 2, expand later)
1. Amazon
2. Walmart

### Pricing tiers on RapidAPI
- Free: 50 requests/day
- Basic ($19/mo): 1,000 requests/day
- Pro ($49/mo): 10,000 requests/day + history endpoint

## Steps to Launch

1. **Setup** — project structure, FastAPI skeleton, Playwright scraper base
2. **Scrapers** — Amazon product page scraper, Walmart scraper (price + title + availability)
3. **Storage** — PostgreSQL schema for products + price history, Redis cache layer
4. **API** — wire scrapers into FastAPI endpoints, add rate limiting
5. **Deploy** — containerize with Docker, deploy to Railway
6. **RapidAPI listing** — create listing, define pricing tiers, write docs
7. **Test & monitor** — verify scrapers survive bot detection, set up scraper health alerts

## Risks & Mitigations
- **Bot detection:** Playwright with stealth mode + rotating user agents + delays
- **ToS / legal:** scraping publicly visible prices is widely practiced; no login required
- **Scraper breakage:** retailers change HTML often — build alerts for scraper failures
