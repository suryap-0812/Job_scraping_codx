import argparse

from .pipeline import export_json, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape and filter tech opportunities")
    parser.add_argument("--max-sources", type=int, default=None, help="Limit source count")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds")
    parser.add_argument("--output", type=str, default="data/opportunities.json", help="JSON output path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    items = run_pipeline(max_sources=args.max_sources, timeout=args.timeout)
    output = export_json(items, args.output)
    print(f"Saved {len(items)} opportunities to {output}")


if __name__ == "__main__":
    main()
