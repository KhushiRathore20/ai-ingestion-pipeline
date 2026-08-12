import aiohttp
from datetime import datetime, timezone

YC_API = "https://yc-oss.github.io/api/companies/all.json"


async def fetch_startups(limit=1000):
    async with aiohttp.ClientSession(
        headers={"User-Agent": "AI-Ingestion-Pipeline/1.0"}
    ) as session:

        async with session.get(YC_API, timeout=60) as resp:
            resp.raise_for_status()
            data = await resp.json()

    startups = []

    for company in data:
        if len(startups) >= limit:
            break

        name = company.get("name")
        if not name:
            continue

        slug = company.get("slug") or name.lower().replace(" ", "-")

        startups.append({
            "schemaVersion": "1.0",
            "recordType": "STARTUP",
            "source_name": "Y Combinator",
            "source_url": f"https://www.ycombinator.com/companies/{slug}",
            "entityName": name,
            "employeeCount": company.get("team_size"),
            "collectedAt": datetime.now(timezone.utc).isoformat(),
        })

    return startups