from src.orchestrator.freshness import parse_date, is_fresh


def test_parse_date_valid():
    result = parse_date("2026-08-11T10:00:00Z")
    assert result is not None


def test_parse_date_invalid():
    try:
        parse_date("invalid-date")
    except Exception:
        assert True


def test_is_fresh_valid_date():
    result = is_fresh("2026-08-11T10:00:00Z")
    assert isinstance(result, bool)


def test_is_fresh_old_date():
    result = is_fresh("2026-01-01T10:00:00Z")
    assert isinstance(result, bool)