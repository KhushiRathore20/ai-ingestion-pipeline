import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import re

from src.orchestrator.freshness import parse_date, is_fresh


JOB_FEEDS = {
    "Remote OK": "https://remoteok.com/remote-jobs.rss",
    "We Work Remotely": "https://weworkremotely.com/remote-jobs.rss",
    "Himalayas": "https://himalayas.app/jobs/rss",
    "Jobicy": "https://jobicy.com/?feed=job_feed",
    "Remotive": "https://remotive.com/remote-jobs/feed",
}


def extract_company(title, description):
    text = f"{title or ''} {description or ''}"

    patterns = [
        r"\bat\s+([A-Z][A-Za-z0-9&.\- ]{1,50})",
        r"\bfor\s+([A-Z][A-Za-z0-9&.\- ]{1,50})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return ""


async def fetch_job_feed(session, source_name, feed_url):
    try:
        async with session.get(
            feed_url,
            timeout=30,
            headers={"User-Agent": "AI-Ingestion-Pipeline/1.0"}
        ) as resp:

            if resp.status != 200:
                print(f"{source_name}: HTTP {resp.status}")
                return []

            text = await resp.text()

        root = ET.fromstring(text)
        jobs = []

        for item in root.findall(".//item"):

            title = item.findtext("title") or ""
            link = item.findtext("link") or ""
            description = item.findtext("description") or ""
            pub_date = item.findtext("pubDate")

            if not pub_date:
                continue

            if not is_fresh(pub_date):
                continue

            parsed_date = parse_date(pub_date)

            if not parsed_date:
                continue

            jobs.append({
                "schemaVersion": "1.0",
                "recordType": "JOB",
                "source_name": source_name,
                "source_url": link,
                "company": extract_company(title, description),
                "date": parsed_date.isoformat(),
                "is_remote": True,
                "role_family": title,
                "description": description,
            })

        print(f"{source_name}: {len(jobs)} fresh jobs")
        return jobs

    except Exception as e:
        print(f"Job feed failed: {source_name} -> {e}")
        return []


async def fetch_jobs():

    async with aiohttp.ClientSession() as session:

        tasks = [
            fetch_job_feed(session, name, url)
            for name, url in JOB_FEEDS.items()
        ]

        results = await asyncio.gather(*tasks)

    jobs = []

    for result in results:
        jobs.extend(result)

    # Remove duplicate URLs
    unique_jobs = {}
    for job in jobs:
        if job["source_url"]:
            unique_jobs[job["source_url"]] = job

    return list(unique_jobs.values())