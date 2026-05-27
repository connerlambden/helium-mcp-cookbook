"""Pull the full source-bias corpus from mcp_all_source_biases and print a
top-N comparison across a chosen bias dimension.

Each source comes back with two top-level scores and a nested `bias_values`
dict of 11 named dimensions. Pass any of these as a CLI arg:

  top-level fields  : emotionality_score, prescriptiveness_score
  bias_values keys  : overall credibility, fearful bias, opinion bias,
                      oversimplification bias, appeal to authority bias,
                      covering the response bias, establishment bias,
                      integrity bias, article intelligence,
                      objective sensational bias, bearish bullish bias

Usage:
    python recipes/01_news_bias_dashboard.py
    python recipes/01_news_bias_dashboard.py emotionality_score 15
    python recipes/01_news_bias_dashboard.py "fearful bias" 20
"""
import sys
import requests

ENDPOINT = "https://heliumtrades.com/mcp_all_source_biases/"


def get_score(src: dict, dimension: str):
    if dimension in src:
        return src[dimension]
    bv = src.get("bias_values") or {}
    return bv.get(dimension)


def main(dimension: str = "overall credibility", top_n: int = 10) -> None:
    resp = requests.get(ENDPOINT, timeout=30)
    resp.raise_for_status()
    sources = resp.json().get("sources", [])

    rows = []
    for s in sources:
        score = get_score(s, dimension)
        if isinstance(score, (int, float)):
            rows.append((s.get("source_name", "?"), score, s.get("articles_analyzed", 0)))

    if not rows:
        print(f"No source had a numeric '{dimension}' score.")
        print("Try one of: emotionality_score, prescriptiveness_score,")
        print("'overall credibility', 'fearful bias', 'opinion bias', 'integrity bias', etc.")
        sys.exit(1)

    rows.sort(key=lambda r: r[1], reverse=True)
    print(f"\nTop {top_n} sources by '{dimension}'  ({len(rows)} sources scored)\n")
    print(f"{'Rank':<5}{'Source':<38}{'Score':<10}{'Articles':<10}")
    print("-" * 63)
    for i, (src, score, n) in enumerate(rows[:top_n], 1):
        print(f"{i:<5}{src[:37]:<38}{score:<10}{n:<10}")


if __name__ == "__main__":
    dim = sys.argv[1] if len(sys.argv) > 1 else "overall credibility"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    main(dim, n)
