import asyncio

from src.crawlers.arxiv import fetch_arxiv
from src.crawlers.jobs import fetch_jobs
from src.crawlers.news import fetch_news

from src.storage.csv_export import (
    export_papers,
    export_jobs,
    export_news,
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

    print("\nAll ingestion completed!")
    print("Files:")
    print("output/papers.csv")
    print("output/jobs.csv")
    print("output/news.csv")


if __name__ == "__main__":
    asyncio.run(run())