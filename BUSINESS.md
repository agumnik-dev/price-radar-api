# PriceRadar — Business Model

## The Idea
PriceRadar is a REST API that provides real-time Amazon product prices, availability status,
and historical price data. Developers and businesses subscribe to use it instead of building
and maintaining their own scrapers.

## Target Customers
- **Dropshippers** — need to monitor competitor prices and margins daily
- **Small retailers** — track competitor pricing on Amazon to stay competitive
- **Price comparison apps** — need structured price data without maintaining scrapers
- **E-commerce analytics tools** — embed price tracking into their dashboards
- **Developers** — building apps that need Amazon price data without dealing with bot detection

## Distribution Strategy
Listed on **RapidAPI marketplace** — zero active marketing required.
Developers search RapidAPI for price/scraping APIs and subscribe directly.
RapidAPI handles billing, metering, and customer discovery automatically.

## Revenue Model
Monthly subscriptions via RapidAPI:

| Plan  | Price     | Quota          | Target customer              |
|-------|-----------|----------------|------------------------------|
| Free  | $0        | 20 req/day     | Evaluation, hobby projects   |
| Basic | $19/month | 1,000 req/day  | Small apps, individual sellers |
| Pro   | $49/month | 10,000 req/day | Growing apps, small agencies |
| Ultra | $99/month | 50,000 req/day | High-volume businesses       |

RapidAPI takes ~20% platform fee. Net revenue per subscriber:
- Basic: ~$15/month
- Pro: ~$39/month
- Ultra: ~$79/month

## Path to $500/month MRR
- 5 Basic + 5 Pro subscribers = $75 + $195 = ~$270/month net
- 10 Basic + 5 Pro + 2 Ultra subscribers = ~$500/month net
- Realistic 3-month target given RapidAPI organic discovery

## Cost Structure (monthly)
- Railway hosting (API + Postgres + Redis): ~$10/month
- ScraperAPI: free tier (5,000 req/month) → $49/month at scale
- Total at launch: ~$10/month

## Competitive Advantage
- **ScraperAPI autoparse** handles bot detection — no fragile HTML parsers
- **Price history** stored in PostgreSQL — most competitors return only current price
- **Low price point** — enterprise tools charge $200+/month for similar data
- **RapidAPI marketplace** — instant access to millions of developers

## Growth Plan
1. Launch with Amazon (working)
2. Add Best Buy / Target when revenue covers additional ScraperAPI costs
3. Add bulk ASIN lookup endpoint (high-value feature for retailers)
4. Add price drop webhook notifications (increases stickiness)
