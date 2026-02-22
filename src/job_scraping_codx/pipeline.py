import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .models import Opportunity, Source
from .scraper import extract_opportunities, fetch_html
from .sources import default_sources
from .tech_filter import relevance_label, relevance_score


def fingerprint(opportunity: Opportunity) -> str:
    base = "|".join(
        [
            opportunity.title.strip().lower(),
            opportunity.company_or_organizer.strip().lower(),
            opportunity.opportunity_type.strip().lower(),
            opportunity.apply_url.strip().lower(),
        ]
    )
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


def dedupe(opportunities: list[Opportunity]) -> list[Opportunity]:
    seen: set[str] = set()
    unique: list[Opportunity] = []
    for item in opportunities:
        key = fingerprint(item)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def process_source(source: Source, timeout: int = 15) -> list[Opportunity]:
    html = fetch_html(source.url, timeout=timeout)
    items = extract_opportunities(source, html)
    for item in items:
        text = f"{item.title} {item.description}"
        score = relevance_score(text)
        item.relevance_score = score
        item.relevance_label = relevance_label(score)
    return [i for i in items if i.relevance_label in {"tech_relevant", "needs_review"}]


def run_pipeline(max_sources: int | None = None, timeout: int = 15) -> list[Opportunity]:
    sources = default_sources()
    if max_sources is not None:
        sources = sources[:max_sources]

    collected: list[Opportunity] = []
    for source in sources:
        try:
            collected.extend(process_source(source, timeout=timeout))
        except Exception:
            continue

    return dedupe(collected)


def export_json(opportunities: list[Opportunity], output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(item) for item in opportunities]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
