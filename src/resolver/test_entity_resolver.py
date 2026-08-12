from src.resolver.entity_resolver import resolve_entity


tests = [
    "OpenAI",
    "Open AI",
    "OpenAI Inc.",
    "Google",
    "Google DeepMind",
    "HuggingFace",
    "NVIDIA Corporation",
]


for name in tests:
    print(f"{name} -> {resolve_entity(name)}")