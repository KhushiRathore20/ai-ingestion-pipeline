from src.orchestrator.freshness import parse_date, is_fresh


dates = [
    "2026-08-11T10:00:00Z",
    "2026-01-01T10:00:00Z",
    "invalid-date",
]


for date in dates:
    print(date)
    print("Parsed:", parse_date(date))
    print("Fresh:", is_fresh(date))
    print()