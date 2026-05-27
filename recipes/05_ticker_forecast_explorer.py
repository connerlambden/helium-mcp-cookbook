"""Pull Helium's ML-driven bullish / bearish case for each ticker in a
short watchlist, strip HTML for readability, and print a side-by-side
comparison.

Underlying endpoint:
    GET https://heliumtrades.com/mcp_ticker/?ticker=NVDA

Returned fields used here: ticker, name, latest_price, bullish_case,
bearish_case, page_url.

Usage:
    python recipes/05_ticker_forecast_explorer.py             # default watchlist
    python recipes/05_ticker_forecast_explorer.py NVDA AAPL META TSLA SPY
"""
import re
import sys
import textwrap

import requests

ENDPOINT = "https://heliumtrades.com/mcp_ticker/"
DEFAULT_WATCHLIST = ["NVDA", "AAPL", "META", "TSLA", "SPY"]

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_html(s: str) -> str:
    if not s:
        return ""
    return WS_RE.sub(" ", TAG_RE.sub("", str(s))).strip()


def main(tickers: list) -> None:
    for tk in tickers:
        resp = requests.get(ENDPOINT, params={"ticker": tk}, timeout=30)
        if resp.status_code != 200:
            print(f"\n{tk}: HTTP {resp.status_code}")
            continue
        data = resp.json()
        if "error" in data:
            print(f"\n{tk}: {data['error']}")
            continue

        name = data.get("name", tk)
        price = data.get("latest_price", "?")
        bull = strip_html(data.get("bullish_case", ""))
        bear = strip_html(data.get("bearish_case", ""))
        url = data.get("page_url", "")

        print(f"\n{'=' * 70}")
        print(f"{tk} - {name}   latest ${price}")
        print("=" * 70)
        if bull:
            print("\nBULL CASE")
            print(textwrap.fill(bull, 70))
        if bear:
            print("\nBEAR CASE")
            print(textwrap.fill(bear, 70))
        if url:
            print(f"\nFull forecast: {url}")


if __name__ == "__main__":
    watchlist = sys.argv[1:] or DEFAULT_WATCHLIST
    main([t.upper() for t in watchlist])
