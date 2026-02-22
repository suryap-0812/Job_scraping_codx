from html.parser import HTMLParser
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from .models import Opportunity, Source


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._current_href = ""
        self._capture_text = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = dict(attrs)
        self._current_href = attrs_dict.get("href", "") or ""
        self._capture_text = True

    def handle_data(self, data: str) -> None:
        if self._capture_text and self._current_href:
            text = " ".join(data.split())
            if text:
                self.links.append((self._current_href, text))

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self._capture_text = False
            self._current_href = ""


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    clean_query = [(k, v) for k, v in parse_qsl(parsed.query) if not k.startswith("utm_")]
    canonical_query = urlencode(clean_query)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, canonical_query, ""))


def fetch_html(url: str, timeout: int = 15) -> str:
    request = Request(url, headers={"User-Agent": "job-scraping-codx/0.1"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def detect_type(text: str) -> str:
    lowered = text.lower()
    if "hackathon" in lowered:
        return "hackathon"
    if "intern" in lowered:
        return "internship"
    if "job" in lowered or "engineer" in lowered or "developer" in lowered:
        return "job"
    if "apply" in lowered or "form" in lowered or "register" in lowered:
        return "form"
    return "event"


def extract_opportunities(source: Source, html: str) -> list[Opportunity]:
    parser = LinkCollector()
    parser.feed(html)

    opportunities: list[Opportunity] = []
    for href, text in parser.links:
        lowered = text.lower()
        if not any(token in lowered for token in ("job", "engineer", "developer", "intern", "hackathon", "apply")):
            continue
        apply_url = canonicalize_url(urljoin(source.url, href))
        opportunities.append(
            Opportunity(
                source_name=source.name,
                source_url=source.url,
                title=text,
                company_or_organizer="unknown",
                opportunity_type=detect_type(text),
                apply_url=apply_url,
                description=text,
            )
        )
    return opportunities
