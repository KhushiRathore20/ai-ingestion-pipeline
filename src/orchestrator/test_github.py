import asyncio
import aiohttp

from src.crawlers.github_metrics import fetch_stars

async def main():
    async with aiohttp.ClientSession() as session:
        stars = await fetch_stars(
            session,
            "https://github.com/openai/whisper"
        )

        print("GitHub stars:", stars)

asyncio.run(main())