# AI Ingestion Pipeline

Production-grade asynchronous ingestion pipeline for collecting and normalizing AI ecosystem data.

## Data Sources

The pipeline collects:

- Research papers from arXiv
- Remote jobs from multiple job boards
- News articles
- AI startups
- AI products and tools from SaaSHub

## Features

- Asynchronous HTTP crawling using `aiohttp`
- Concurrent ingestion from multiple sources
- Retry and rate-limit handling
- Freshness filtering
- Entity resolution
- GitHub metrics enrichment
- Papers With Code enrichment
- Normalized CSV output
- Pytest test suite
- Modular crawler/orchestrator architecture

## Project Structure

```text
ai-ingestion-pipeline/
│
├── output/
│   ├── papers.csv
│   ├── jobs.csv
│   ├── news.csv
│   ├── startups.csv
│   └── products.csv
│
├── src/
│   ├── crawlers/
│   │   ├── arxiv.py
│   │   ├── github_metrics.py
│   │   ├── jobs.py
│   │   ├── news.py
│   │   ├── paperswithcode.py
│   │   ├── products.py
│   │   └── startups.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── orchestrator/
│   │   ├── pipeline.py
│   │   ├── freshness.py
│   │   └── enrich_papers.py
│   │
│   ├── resolver/
│   │   └── entity_resolver.py
│   │
│   ├── storage/
│   │   └── csv_export.py
│   │
│   └── utils/
│       ├── logging.py
│       └── retry.py
│
├── requirements.txt
├── pytest.ini
└── README.md