import asyncio

from src.orchestrator.enrich_papers import enrich_all

papers = [
    {
        "title": "Attention Is All You Need",
        "github_url": "https://github.com/huggingface/transformers"
    }
]

async def main():
    enriched = await enrich_all(papers)
    print(enriched)

asyncio.run(main())