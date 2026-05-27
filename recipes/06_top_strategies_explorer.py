"""Pull Helium's top short-volatility and long-volatility option-strategy
lists and print a compact table.

Underlying endpoint:
    GET https://heliumtrades.com/mcp_top_strategies/

Response shape: { sort, short_volatility: [...], long_volatility: [...] }

Each entry contains ticker, name, latest_price, page_url, and embedded
bullish/bearish narrative HTML. This recipe shows the ticker + price
table only; modify if you want to print the narratives too.

Usage:
    python recipes/06_top_strategies_explorer.py
    python recipes/06_top_strategies_explorer.py 15
"""
import sys
import requests

ENDPOINT = "https://heliumtrades.com/mcp_top_strategies/"


def main(n: int = 10) -> None:
    resp = requests.get(ENDPOINT, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    short_vol = data.get("short_volatility", [])
    long_vol = data.get("long_volatility", [])

    print(f"\nSort: {data.get('sort', '?')}\n")

    def show(label: str, rows: list) -> None:
        print(f"--- {label} (top {n} of {len(rows)}) ---")
        print(f"{'Ticker':<8}{'Name':<32}{'Price':<10}{'URL'}")
        print("-" * 100)
        for r in rows[:n]:
            tk = r.get("ticker", "?")
            name = r.get("name", "?")[:31]
            price = r.get("latest_price", "?")
            url = r.get("page_url", "")
            print(f"{tk:<8}{name:<32}{price:<10}{url}")
        print()

    show("SHORT-VOLATILITY CANDIDATES", short_vol)
    show("LONG-VOLATILITY CANDIDATES", long_vol)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
