from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Source:
    name: str
    url: str
    source_kind: str
    crawl_interval_minutes: int = 360


@dataclass
class Opportunity:
    source_name: str
    source_url: str
    title: str
    company_or_organizer: str
    opportunity_type: str
    apply_url: str
    description: str
    skills: list[str] = field(default_factory=list)
    posted_at: str | None = None
    relevance_score: float = 0.0
    relevance_label: str = "unknown"
    first_seen_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
