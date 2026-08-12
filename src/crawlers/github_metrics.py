import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=30),
)
async def fetch_stars(session, github_url):
    if not github_url:
        return None

    parts = github_url.rstrip("/").split("/")

    # Need a repository URL: https://github.com/owner/repo
    if len(parts) < 5:
        return None

    owner = parts[-2]
    repo = parts[-1]

    api = f"https://api.github.com/repos/{owner}/{repo}"

    async with session.get(api, timeout=20) as resp:
        if resp.status == 404:
            return None

        if resp.status == 403:
            raise Exception("GitHub rate limit")

        resp.raise_for_status()

        data = await resp.json()

        return data.get("stargazers_count")