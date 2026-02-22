# Job Scraping CODX (MVP)

A production-oriented starter project that continuously discovers and filters **software/tech-only** opportunities:
- Jobs
- Internships
- Hackathons
- Application forms

## What is implemented
- Source registry model and crawler settings.
- HTTP fetcher.
- Opportunity extraction from HTML page title/meta + links.
- Tech relevance scoring and filtering.
- URL canonicalization + deduplication fingerprinting.
- JSON export pipeline.
- CLI entrypoint.
- Unit tests for filtering, dedupe, and extraction behavior.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
job-scraper --max-sources 5 --output data/opportunities.json
```

## CLI
```bash
job-scraper --help
```
Options:
- `--max-sources`: limit number of configured sources to scrape.
- `--timeout`: HTTP timeout in seconds.
- `--output`: JSON file path for results.

## Notes
- This MVP intentionally uses standard library only to stay portable.
- For dynamic websites, extend `fetch_html` with Playwright integration.
- Respect robots.txt and source terms before production rollout.
