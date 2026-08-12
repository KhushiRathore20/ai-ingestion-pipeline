import aiohttp
import asyncio
import ssl
import xml.etree.ElementTree as ET


ARXIV_API = (
    "https://export.arxiv.org/api/query?"
    "search_query=cat:cs.AI&start={start}&max_results={count}"
)


async def fetch_page(session, start: int, count: int = 100):
    url = ARXIV_API.format(start=start, count=count)

    for attempt in range(5):
        try:
            async with session.get(
                url,
                timeout=60,
                headers={
                    "User-Agent": "AI-Ingestion-Pipeline/1.0"
                },
            ) as resp:

                if resp.status == 429:
                    wait_time = 10 * (attempt + 1)

                    print(
                        f"ArXiv rate limit (429) at start={start}. "
                        f"Retrying in {wait_time}s..."
                    )

                    await asyncio.sleep(wait_time)
                    continue

                resp.raise_for_status()

                return await resp.text()

        except Exception as e:

            if attempt == 4:
                print(
                    f"ArXiv page failed start={start}: {e}"
                )
                return None

            wait_time = 5 * (attempt + 1)

            print(
                f"ArXiv request failed at start={start}. "
                f"Retrying in {wait_time}s..."
            )

            await asyncio.sleep(wait_time)

    return None


def parse_feed(xml_text: str):

    if not xml_text:
        return []

    root = ET.fromstring(xml_text)

    ns = {
        "a": "http://www.w3.org/2005/Atom"
    }

    papers = []

    for entry in root.findall("a:entry", ns):

        title_element = entry.find("a:title", ns)
        published_element = entry.find("a:published", ns)
        id_element = entry.find("a:id", ns)

        if title_element is None or id_element is None:
            continue

        title = title_element.text.strip()

        authors = []

        for author in entry.findall("a:author", ns):

            name = author.find("a:name", ns)

            if name is not None and name.text:
                authors.append(name.text.strip())

        paper_url = id_element.text.strip()

        pdf_url = None

        for link in entry.findall("a:link", ns):

            if link.attrib.get("title") == "pdf":
                pdf_url = link.attrib.get("href")
                break

        published = ""

        if published_element is not None and published_element.text:
            published = published_element.text.strip()

        papers.append({
            "title": title,
            "authors": authors,
            "paper_url": paper_url,
            "pdf_url": pdf_url,
            "published_date": published,
        })

    return papers


async def fetch_arxiv(total=1000):

    ssl_context = ssl.create_default_context()

    # Keeps compatibility with the SSL setup
    # that was already working in your project.
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(
        ssl=ssl_context
    )

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = []

        for start in range(0, total, 100):

            tasks.append(
                fetch_page(
                    session,
                    start,
                    100
                )
            )

            # Prevent ArXiv rate limiting
            await asyncio.sleep(2)

        pages = await asyncio.gather(
            *tasks
        )

    papers = []

    for page in pages:

        if page:
            papers.extend(
                parse_feed(page)
            )

    # Keep exactly the requested number
    return papers[:total]