import asyncio
import aiohttp
import xml.etree.ElementTree as ET

from src.orchestrator.freshness import parse_date, is_fresh


NEWS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "MIT Technology Review": "https://www.technologyreview.com/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/",
    "The Decoder": "https://the-decoder.com/feed/",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
}


async def fetch_news_feed(session, source_name, feed_url):
    try:
        async with session.get(feed_url, timeout=30) as resp:
            if resp.status != 200:
                return []

            text = await resp.text()

        root = ET.fromstring(text)
        news = []

        for item in root.findall(".//item"):
            title = item.findtext("title")
            link = item.findtext("link")
            description = item.findtext("description")
            pub_date = item.findtext("pubDate")

            if not pub_date or not is_fresh(pub_date):
                continue

            news.append({
                "schemaVersion": "1.0",
                "recordType": "NEWS",
                "source_name": source_name,
                "source_url": link,
                "title": title or "",
                "content": description or "",
                "published_date": parse_date(pub_date).isoformat(),
            })

        return news

    except Exception as e:
        print(f"News feed failed: {source_name} -> {e}")
        return []


async def fetch_news():
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_news_feed(session, name, url)
            for name, url in NEWS_FEEDS.items()
        ]

        results = await asyncio.gather(*tasks)

    news = []

    for result in results:
        news.extend(result)

    return news