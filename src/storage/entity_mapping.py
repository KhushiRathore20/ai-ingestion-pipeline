import csv
import os

from src.resolver.entity_resolver import resolve_with_log


INPUT_FILE = "output/startups.csv"
OUTPUT_FILE = "output/entity_mapping.csv"


def create_entity_mapping():
    names = []

    with open(INPUT_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get("entityName", "").strip()

            if name:
                names.append(name)

    # Remove duplicate names while preserving order
    names = list(dict.fromkeys(names))

    mappings = resolve_with_log(names)

    os.makedirs("output", exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["raw_name", "canonical_name"],
        )

        writer.writeheader()
        writer.writerows(mappings)

    print(f"Created {OUTPUT_FILE}")
    print(f"Mapped entities: {len(mappings)}")


if __name__ == "__main__":
    create_entity_mapping()