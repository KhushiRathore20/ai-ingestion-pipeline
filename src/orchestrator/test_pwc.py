import asyncio
import aiohttp

from src.crawlers.paperswithcode import fetch_github_from_pwc

async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://paperswithcode.com/paper/attention-is-all-you-need"
        github = await fetch_github_from_pwc(session, url)
        print(github)

asyncio.run(main())