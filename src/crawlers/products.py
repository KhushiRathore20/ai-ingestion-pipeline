import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin


BASE_URL = "https://www.saashub.com"
AI_URL = "https://www.saashub.com/v/ai"


async def fetch_products(limit=1000):
    products = []
    seen = set()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(
        headers=headers,
        timeout=timeout
    ) as session:

        for page in range(1, 51):

            if len(products) >= limit:
                break

            url = AI_URL if page == 1 else f"{AI_URL}?page={page}"

            try:
                async with session.get(url) as resp:

                    if resp.status != 200:
                        print(f"SaaSHub HTTP {resp.status}: {url}")
                        continue

                    html = await resp.text()

            except Exception as e:
                print(f"SaaSHub failed: {url} -> {e}")
                continue

            soup = BeautifulSoup(html, "html.parser")

            for a in soup.find_all("a", href=True):

                href = a["href"]
                name = a.get_text(" ", strip=True)

                # Actual SaaSHub product pages
                if not href.endswith("-alternatives"):
                    continue

                if href.startswith("/alternatives/"):
                    continue

                if not href.startswith("/"):
                    continue

                if not name or len(name) < 2:
                    continue

                full_url = urljoin(BASE_URL, href)

                if full_url in seen:
                    continue

                seen.add(full_url)

                products.append({
                    "schemaVersion": "1.0",
                    "recordType": "PRODUCT",
                    "source_name": "SaaSHub",
                    "source_url": full_url,
                    "productName": name,
                    "startupName": "",
                    "pricingModel": "UNKNOWN",
                    "collectedAt": datetime.now(
                        timezone.utc
                    ).isoformat(),
                })

                if len(products) >= limit:
                    break

    print(f"SaaSHub products found: {len(products)}")

    return products[:limit]

