import re


CANONICAL_ENTITIES = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google": "Google",
    "google deepmind": "Google DeepMind",
    "microsoft": "Microsoft",
    "meta": "Meta",
    "meta ai": "Meta",
    "nvidia": "NVIDIA",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
}


def normalize_name(name: str) -> str:
    if not name:
        return ""

    name = name.lower().strip()

    name = re.sub(
        r"\b(incorporated|inc|corp|corporation|ltd|limited|llc|plc)\b",
        "",
        name,
    )

    name = re.sub(r"[^a-z0-9]+", " ", name)

    return " ".join(name.split())


def resolve_entity(name: str) -> str:
    normalized = normalize_name(name)

    if normalized in CANONICAL_ENTITIES:
        return CANONICAL_ENTITIES[normalized]

    return name.strip()


def resolve_with_log(names):
    results = []

    for raw_name in names:
        canonical = resolve_entity(raw_name)

        results.append({
            "raw_name": raw_name,
            "canonical_name": canonical,
        })

    return results