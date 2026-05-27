"""Semantic-search Helium's meme corpus and print captions + OCR text +
like counts + image URLs for each result. Useful for cultural-context
queries that pair with the news-bias data.

Underlying endpoint:
    GET https://heliumtrades.com/mcp_meme_search/?q=tariffs

Each result has: id, caption, ocr, image, source, num_likes, date,
is_video, rank.

Usage:
    python recipes/07_meme_search.py "tariffs"
    python recipes/07_meme_search.py "ai regulation" 5
"""
import sys
import textwrap

import requests

ENDPOINT = "https://heliumtrades.com/mcp_meme_search/"


def main(query: str, n: int = 8) -> None:
    resp = requests.get(ENDPOINT, params={"q": query, "limit": n}, timeout=30)
    resp.raise_for_status()
    results = resp.json().get("results", [])

    if not results:
        print(f"No memes found for {query!r}.")
        return

    print(f"\nTop {len(results[:n])} memes for {query!r}:\n")
    for i, r in enumerate(results[:n], 1):
        ocr = (r.get("ocr") or "").replace("\n", " / ")
        print(f"[{i}] likes={r.get('num_likes', '?')}  rank={r.get('rank', '?')}  "
              f"source={r.get('source', '?')}  date={r.get('date', '?')[:10]}")
        if ocr:
            print(textwrap.fill(f"    OCR: {ocr}", 72, subsequent_indent="    "))
        print(f"    image: {r.get('image', '')}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python 07_meme_search.py "your query" [n]')
        sys.exit(1)
    q = sys.argv[1]
    nn = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    main(q, nn)
