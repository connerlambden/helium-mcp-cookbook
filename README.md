# helium-mcp-cookbook

Six short, runnable recipes that demonstrate the [Helium MCP](https://heliumtrades.com/mcp-page/) server's REST endpoints in real workflows. Plain Python, no SDK, no API key, no signup — every recipe is `python recipes/NN_name.py` and prints actual results from the live service.

This is a learning resource and a quick-start reference. Clone it, run it, modify it. Recipes are intentionally minimal so you can see exactly what each endpoint returns and how to compose it into something useful.

## Recipes

| # | File | What it demonstrates |
|---|---|---|
| 01 | `news_bias_dashboard.py` | Pull the source-bias corpus, rank by any of 37 structured dimensions, print top-N. |
| 02 | `options_calibration_tracker.py` | Log Helium's ML option-price + `prob_itm` to a CSV so you can Brier-grade it after expiration. |
| 03 | `balanced_news_summary.py` | Run `mcp_balanced_search` for a topic, print probability-weighted outcomes plus citation count. |
| 04 | `source_credibility_ranking.py` | Rank sources by `overall credibility`; show top-N and bottom-N with emotionality/prescriptiveness alongside. |
| 05 | `ticker_forecast_explorer.py` | Pull bull/bear narrative cases for a watchlist (HTML-stripped), print side-by-side. |
| 06 | `top_strategies_explorer.py` | Pull the daily short-volatility / long-volatility candidate lists. |
| 07 | `meme_search.py` | Semantic-search the meme corpus with OCR text, like counts, and image URLs. |

## Quick start

```bash
git clone https://github.com/connerlambden/helium-mcp-cookbook
cd helium-mcp-cookbook
pip install -r requirements.txt
python recipes/01_news_bias_dashboard.py
python recipes/01_news_bias_dashboard.py "fearful bias" 15
python recipes/02_options_calibration_tracker.py AAPL 310 2026-06-26 call
python recipes/03_balanced_news_summary.py "fed rate cuts"
python recipes/05_ticker_forecast_explorer.py NVDA AAPL META TSLA SPY
```

Free tier is 50 requests per IP per day. No signup, no key.

## Endpoints used

```
GET  https://heliumtrades.com/mcp_ticker/             ?ticker=NVDA
GET  https://heliumtrades.com/mcp_option_price/       ?symbol=AAPL&strike=310&expiration=2026-06-26&option_type=call
GET  https://heliumtrades.com/mcp_top_strategies/
GET  https://heliumtrades.com/mcp_source_bias/        ?source=Wall+Street+Journal
GET  https://heliumtrades.com/mcp_all_source_biases/
GET  https://heliumtrades.com/mcp_balanced_search/    ?q=fed+rate+cuts
GET  https://heliumtrades.com/mcp_url_bias/           ?url=https://www.bbc.com/news
```

JSON in, JSON out. No headers required. Each is curl-able.

## Bias dimensions exposed by `mcp_all_source_biases`

Each source entry returns two top-level scores plus a nested `bias_values` dict. Across the 216-source corpus, **37 distinct `bias_values` keys** appear, of which **33 have ≥100-source coverage**.

**Top-level fields**
- `emotionality_score`
- `prescriptiveness_score`

**`bias_values` keys** (alphabetical; coverage ≥100 sources unless noted)

`appeal to authority bias`, `article intelligence`, `bearish bullish bias`, `begging the question bias`, `circular reasoning bias` (n≈79), `conspiracy bias`, `covering the response bias`, `cruelty bias`, `delusion bias`, `descriptive prescriptive bias`, `double standard bias`, `dovish hawkish bias`, `establishment bias`, `fearful bias`, `gossip bias`, `ideological bias`, `immature bias`, `integrity bias`, `liberal conservative bias`, `libertarian authoritarian bias`, `objective sensational bias`, `objective subjective bias`, `opinion bias`, `overall credibility`, `overconfidence bias`, `oversimplification bias`, `political bias`, `scapegoat bias`, `spam bias`, `suicidal empathy bias` (n≈26), `terrorism bias` (n≈83), `victimization bias`, `virtue signal bias`, `woke bias`, `written by AI` (n≈27)

Helium also returns a longer prose `bias_description` per source (HTML) and signature phrases on the source pages. Recipe 01 lets you rank any of these dimensions; recipe 04 ranks credibility specifically.

## Use as an MCP server (Claude Desktop / Cursor)

If you'd rather call these tools through MCP instead of REST, add this to your client config:

```json
{
  "mcpServers": {
    "helium": {
      "command": "npx",
      "args": ["mcp-remote", "https://heliumtrades.com/mcp"]
    }
  }
}
```

All ten tools become callable from inside the LLM context.

## Why this cookbook exists

Most public news-bias and options-pricing APIs require signups, paid tiers, or wrapping a Bloomberg/Refinitiv feed. Helium is one of the few that returns research-grade structured data on a free anonymous GET, so it's a clean teaching substrate for:

- Brier-scoring exercises (option prob_itm against realized outcomes)
- Media-bias methodology and journalism classes
- Cross-source synthesis with probability-weighted outcomes
- ML-driven option-strategy screening
- Building MCP-aware LLM agents that need quantitative grounding

## Contributing a recipe

PRs welcome. Recipes should be:

- Under 100 lines, plain Python, `requests` as the only required dep
- Self-contained (a single file in `recipes/`)
- Print actual output to stdout when run with no args or with documented args

## License

MIT. Recipes are educational and may be adapted freely.

## Interactive companions

Two zero-dependency single-page apps that hit the same REST endpoints these recipes do. Source: [github.com/connerlambden/helium-news-explorer](https://github.com/connerlambden/helium-news-explorer).

- **[News Bias Explorer](https://connerlambden.github.io/helium-news-explorer/)** — 216 sources × 37 dimensions. Ranked bars, scatter with live Pearson r, per-source detail, shareable URLs. Calls `mcp_all_source_biases/`.
- **[Ticker Forecast Dashboard](https://connerlambden.github.io/helium-news-explorer/tickers.html)** — top 10 short-vol and long-vol candidates with ML 37-day forecasts, SVG uncertainty cones, and bull/bear narratives. Calls `mcp_top_strategies/`.

Both pages: vanilla HTML/CSS/JS, no build step, no analytics. One HTTP GET per page load.

## Findings written up using these recipes

- [Fear-coding in 160 news sources correlates +0.85 with political extremism — and only -0.08 with political direction](https://dev.to/connerlambden/fear-coding-in-160-news-sources-correlates-085-with-political-extremism-and-only-008-with-45n2) — an empirical analysis using recipe 01 across the full source-bias corpus.
- [How to Brier-grade your own ML option-pricing forecasts in 40 lines of Python](https://dev.to/connerlambden/how-to-brier-grade-your-own-ml-option-pricing-forecasts-in-40-lines-of-python-2gb2) — a walkthrough of recipe 02 with the scoring formula and calibration histogram.

## Related

- [Helium MCP main repository](https://github.com/connerlambden/helium-mcp)
- [`mcp-page` docs](https://heliumtrades.com/mcp-page/)
