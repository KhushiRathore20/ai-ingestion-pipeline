import asyncio

from src.crawlers.arxiv import fetch_arxiv
from src.crawlers.jobs import fetch_jobs
from src.crawlers.news import fetch_news
from src.crawlers.startups import fetch_startups
from src.crawlers.products import fetch_products

from src.storage.csv_export import (
    export_papers,
    export_jobs,
    export_news,
    export_startups,
    export_products,
)


async def run():

    print("Fetching research papers...")
    papers = await fetch_arxiv(total=1000)
    export_papers(papers)
    print(f"Exported {len(papers)} papers")

    print("\nFetching jobs...")
    jobs = await fetch_jobs()
    export_jobs(jobs)
    print(f"Exported {len(jobs)} jobs")

    print("\nFetching news...")
    news = await fetch_news()
    export_news(news)
    print(f"Exported {len(news)} news articles")

    print("\nFetching startups...")
    startups = await fetch_startups(1000)
    export_startups(startups)
    print(f"Exported {len(startups)} startups")

    print("\nFetching products...")
    products = await fetch_products(1000)
    export_products(products)
    print(f"Exported {len(products)} products")

    print("\nAll ingestion completed!")
    print("Files:")
    print("output/papers.csv")
    print("output/jobs.csv")
    print("output/news.csv")
    print("output/startups.csv")
    print("output/products.csv")


if __name__ == "__main__":
    asyncio.run(run())