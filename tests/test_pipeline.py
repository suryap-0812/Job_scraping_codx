from job_scraping_codx.models import Opportunity
from job_scraping_codx.pipeline import dedupe


def test_dedupe_removes_identical_records() -> None:
    base = Opportunity(
        source_name="S",
        source_url="https://example.com",
        title="Backend Developer",
        company_or_organizer="ACME",
        opportunity_type="job",
        apply_url="https://example.com/apply",
        description="Backend role",
    )
    dup = Opportunity(**base.to_dict())
    unique = dedupe([base, dup])
    assert len(unique) == 1
