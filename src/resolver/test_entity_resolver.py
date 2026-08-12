from src.resolver.entity_resolver import resolve_entity


def test_openai_resolution():
    result = resolve_entity("OpenAI")
    assert result is not None


def test_open_ai_resolution():
    result = resolve_entity("Open AI")
    assert result is not None


def test_google_resolution():
    result = resolve_entity("Google")
    assert result is not None


def test_huggingface_resolution():
    result = resolve_entity("HuggingFace")
    assert result is not None


def test_nvidia_resolution():
    result = resolve_entity("NVIDIA Corporation")
    assert result is not None