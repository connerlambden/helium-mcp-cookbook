"""Pull balanced-news synthesis results from mcp_balanced_search and print
the summary, takeaway, probability-weighted outcomes, and citation count
for each result.

The endpoint returns a `results` list. Each entry includes:
  title, summary, takeaway, context, evidence, potential_outcomes,
  relevant_tickers, num_sources, page_url, date, category, rank

`potential_outcomes` is a JSON-encoded string of outcome statements (each
with an embedded probability). This recipe parses it best-effort.

Usage:
    python recipes/03_balanced_news_summary.py "fed rate cuts"
    python recipes/03_balanced_news_summary.py "ai regulation"
"""
import json
import re
import sys
import textwrap

import requests

ENDPOINT = "https://heliumtrades.com/mcp_balanced_search/"


def parse_outcomes(raw):
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw]
    try:
        loaded = json.loads(raw)
        if isinstance(loaded, list):
            return [str(x) for x in loaded]
    except Exception:
        pass
    return [s.strip() for s in re.split(r"\s*,\s*", str(raw)) if s.strip()]


def main(query: str, n: int = 3) -> None:
    resp = requests.get(ENDPOINT, params={"q": query}, timeout=60)
    resp.raise_for_status()
    results = resp.json().get("results", [])

    if not results:
        print(f"No results for {query!r}.")
        return

    print(f"\n{'=' * 70}\nBalanced synthesis: {query!r}  ({len(results)} results)\n{'=' * 70}")

    for i, r in enumerate(results[:n], 1):
        print(f"\n[{i}] {r.get('title', '?')}")
        print(f"    date={r.get('date', '?')}  sources={r.get('num_sources', '?')}  "
              f"tickers={r.get('relevant_tickers', '?')}")

        summary = r.get("summary") or r.get("simple_title") or ""
        if summary:
            print(textwrap.fill(f"    SUMMARY: {summary}", 72, subsequent_indent="    "))

        takeaway = r.get("takeaway") or ""
        if takeaway:
            print(textwrap.fill(f"    TAKEAWAY: {takeaway}", 72, subsequent_indent="    "))

        outcomes = parse_outcomes(r.get("potential_outcomes"))
        if outcomes:
            print("    OUTCOMES:")
            for o in outcomes[:4]:
                print(textwrap.fill(f"      - {o}", 72, subsequent_indent="        "))

        print(f"    URL: {r.get('page_url', '?')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python 03_balanced_news_summary.py "your query"')
        sys.exit(1)
    main(" ".join(sys.argv[1:]))
