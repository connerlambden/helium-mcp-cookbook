# helium-mcp-cookbook

Six short, runnable recipes that demonstrate the [Helium MCP](https://heliumtrades.com/mcp-page/) server's REST endpoints in real workflows. Plain Python, no SDK, no API key, no signup — every recipe is `python recipes/NN_name.py` and prints actual results from the live service.

This is a learning resource and a quick-start reference. Clone it, run it, modify it. Recipes are intentionally minimal so you can see exactly what each endpoint returns and how to compose it into something useful.

## Recipes

| # | File | What it demonstrates |
|---|---|---|
| 01 | `news_bias_dashboard.py` | Pull the source-bias corpus, rank by any structured dimension, print top-N. |
| 02 | `options_calibration_tracker.py` | Log Helium's ML option-price + `prob_itm` to a CSV so you can Brier-grade it after expiration. |
| 03 | `balanced_news_summary.py` | Run `mcp_search` for a topic, print probability-weighted outcomes plus citation count. |
| 04 | `source_credibility_ranking.py` | Rank sources by `overall credibility`; show top-N and bottom-N with emotionality/prescriptiveness alongside. |
| 05 | `ticker_forecast_explorer.py` | Pull bull/bear narrative cases for a watchlist (HTML-stripped), print side-by-side. |
| 06 | `top_strategies_explorer.py` | Pull the daily short-volatility / long-volatility candidate lists. |

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

## Bias dimensions actually exposed by `mcp_all_source_biases`

Each source entry returns two top-level scores plus a nested `bias_values` dict. The dimensions you can rank or filter on:

**Top-level fields**
- `emotionality_score`
- `prescriptiveness_score`

**`bias_values` keys**
- `overall credibility`
- `fearful bias`
- `opinion bias`
- `oversimplification bias`
- `appeal to authority bias`
- `covering the response bias`
- `establishment bias`
- `integrity bias`
- `article intelligence`
- `objective sensational bias`
- `bearish bullish bias`

Helium also returns a longer prose `bias_description` per source (HTML) and signature phrases on the source pages. The recipes here focus on the structured queryable dimensions.

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

## Related

- [Helium MCP main repository](https://github.com/connerlambden/helium-mcp)
- [`mcp-page` docs](https://heliumtrades.com/mcp-page/)
