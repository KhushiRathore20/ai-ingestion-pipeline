import aiohttp
from bs4 import BeautifulSoup

async def fetch_github_from_pwc(session, pwc_url):
    async with session.get(pwc_url, timeout=20) as resp:
        if resp.status != 200:
            return None

        html = await resp.text()

    soup = BeautifulSoup(html, "lxml")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "github.com" not in href:
            continue

        if href.startswith("//"):
            href = "https:" + href

        # We only accept URLs with owner/repository
        parts = href.rstrip("/").split("/")

        if len(parts) >= 5:
            return "/".join(parts[:5])

    return None