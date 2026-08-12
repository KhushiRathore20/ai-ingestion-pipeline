from pydantic import BaseModel
from typing import List, Optional

class ResearchPaper(BaseModel):
    schemaVersion: str = "1.0"
    recordType: str = "RESEARCH_PAPER"

    title: str
    authors: List[str]

    paper_url: str
    pdf_url: Optional[str] = None

    github_url: Optional[str] = None
    github_stars: Optional[int] = None

    published_date: str