import csv
import os


def export_papers(papers, path="output/papers.csv"):
    os.makedirs("output", exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "title",
                "authors",
                "paper_url",
                "pdf_url",
                "published_date",
            ],
        )

        writer.writeheader()

        for p in papers:
            writer.writerow({
                "title": p.get("title", ""),
                "authors": "; ".join(p.get("authors", [])),
                "paper_url": p.get("paper_url", ""),
                "pdf_url": p.get("pdf_url", ""),
                "published_date": p.get("published_date", ""),
            })


def export_jobs(jobs, path="output/jobs.csv"):
    os.makedirs("output", exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "schemaVersion",
                "recordType",
                "source_name",
                "source_url",
                "company",
                "date",
                "is_remote",
                "role_family",
                "description",
            ],
        )

        writer.writeheader()

        for job in jobs:
            writer.writerow({
                "schemaVersion": job.get("schemaVersion", "1.0"),
                "recordType": job.get("recordType", "JOB"),
                "source_name": job.get("source_name", ""),
                "source_url": job.get("source_url", ""),
                "company": job.get("company", ""),
                "date": job.get("date", ""),
                "is_remote": job.get("is_remote", False),
                "role_family": job.get("role_family", ""),
                "description": job.get("description", ""),
            })


def export_news(news, path="output/news.csv"):
    os.makedirs("output", exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "schemaVersion",
                "recordType",
                "source_name",
                "source_url",
                "title",
                "content",
                "published_date",
            ],
        )

        writer.writeheader()

        for item in news:
            writer.writerow({
                "schemaVersion": item.get("schemaVersion", "1.0"),
                "recordType": item.get("recordType", "NEWS"),
                "source_name": item.get("source_name", ""),
                "source_url": item.get("source_url", ""),
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "published_date": item.get("published_date", ""),
            })


def export_startups(startups, path="output/startups.csv"):
    os.makedirs("output", exist_ok=True)

    if not startups:
        return

    fieldnames = list(startups[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(startups)


def export_products(products, path="output/products.csv"):
    os.makedirs("output", exist_ok=True)

    if not products:
        return

    fieldnames = list(products[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(products)