"""Rank all sources by `bias_values["overall credibility"]` and print the
top-N and bottom-N together with their emotionality and prescriptiveness
scores. Useful for journalism methodology classes, media-literacy
curricula, and source-vetting checklists.

Usage:
    python recipes/04_source_credibility_ranking.py          # top/bottom 10
    python recipes/04_source_credibility_ranking.py 20
"""
import sys

import requests

ENDPOINT = "https://heliumtrades.com/mcp_all_source_biases/"


def main(n: int = 10) -> None:
    resp = requests.get(ENDPOINT, timeout=30)
    resp.raise_for_status()
    sources = resp.json().get("sources", [])

    scored = []
    for s in sources:
        cred = (s.get("bias_values") or {}).get("overall credibility")
        if isinstance(cred, (int, float)):
            scored.append({
                "name": s.get("source_name", "?"),
                "credibility": cred,
                "emotionality": s.get("emotionality_score"),
                "prescriptiveness": s.get("prescriptiveness_score"),
                "n": s.get("articles_analyzed", 0),
            })

    scored.sort(key=lambda r: r["credibility"], reverse=True)
    print(f"\n{len(scored)} sources scored on 'overall credibility'\n")

    def show(label: str, rows: list) -> None:
        print(f"--- {label} ---")
        print(f"{'Source':<32}{'Cred':<8}{'Emot':<8}{'Presc':<8}{'N':<8}")
        print("-" * 64)
        for r in rows:
            cred = r["credibility"]
            emot = r["emotionality"] if r["emotionality"] is not None else "n/a"
            presc = r["prescriptiveness"] if r["prescriptiveness"] is not None else "n/a"
            print(f"{r['name'][:31]:<32}{cred:<8}{str(emot):<8}{str(presc):<8}{r['n']:<8}")
        print()

    show(f"TOP {n} BY CREDIBILITY", scored[:n])
    show(f"BOTTOM {n} BY CREDIBILITY", list(reversed(scored[-n:])))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
