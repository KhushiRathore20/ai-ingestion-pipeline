import asyncio
import aiohttp

from src.crawlers.github_metrics import fetch_stars

async def enrich_paper(paper):
    github = paper.get("github_url")

    if not github:
        paper["github_stars"] = None
        return paper

    async with aiohttp.ClientSession() as session:
        paper["github_stars"] = await fetch_stars(session, github)

    return paper

async def enrich_all(papers):
    tasks = [enrich_paper(p) for p in papers]
    return await asyncio.gather(*tasks)