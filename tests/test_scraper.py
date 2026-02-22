from job_scraping_codx.models import Source
from job_scraping_codx.scraper import canonicalize_url, extract_opportunities


SAMPLE_HTML = """
<html>
  <body>
    <a href='/jobs/backend?utm_source=x'>Backend Engineer Job</a>
    <a href='/careers/sales'>Sales Executive Role</a>
    <a href='https://example.com/hack?utm_medium=y'>AI Hackathon 2026</a>
  </body>
</html>
"""


def test_canonicalize_url_removes_utm_params() -> None:
    url = "https://example.com/jobs?id=10&utm_source=abc&utm_medium=mail"
    assert canonicalize_url(url) == "https://example.com/jobs?id=10"


def test_extract_opportunities_picks_tech_tokens() -> None:
    source = Source(name="Test", url="https://example.com", source_kind="job_board")
    items = extract_opportunities(source, SAMPLE_HTML)
    titles = [i.title for i in items]
    assert "Backend Engineer Job" in titles
    assert "AI Hackathon 2026" in titles
    assert "Sales Executive Role" not in titles
