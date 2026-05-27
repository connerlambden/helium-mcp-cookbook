"""Log Helium's ML option-price + prob_itm forecasts to a CSV so you can
Brier-grade them at expiration.

Each run appends one row with:
    timestamp, symbol, strike, expiration, option_type,
    helium_predicted_price, helium_prob_itm, market_mark (manual),
    realized_outcome (filled in after expiration)

Usage:
    python recipes/02_options_calibration_tracker.py AAPL 310 2026-06-26 call
    python recipes/02_options_calibration_tracker.py NVDA 220 2026-07-17 put
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

import requests

ENDPOINT = "https://heliumtrades.com/mcp_option_price/"
LOG_FILE = Path("calibration_log.csv")


def main(symbol: str, strike: float, expiration: str, option_type: str) -> None:
    params = {
        "symbol": symbol,
        "strike": strike,
        "expiration": expiration,
        "option_type": option_type,
    }
    resp = requests.get(ENDPOINT, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    predicted = data.get("predicted_price")
    prob_itm = data.get("prob_itm")
    data_date = data.get("options_data_date", "?")

    if predicted is None:
        print(f"No prediction returned. Raw response: {data}")
        sys.exit(1)

    is_new = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow([
                "timestamp", "symbol", "strike", "expiration", "option_type",
                "helium_predicted_price", "helium_prob_itm",
                "helium_data_date", "market_mark", "realized_underlying_price",
                "realized_itm", "brier_loss",
            ])
        w.writerow([
            datetime.utcnow().isoformat(timespec="seconds"),
            symbol, strike, expiration, option_type,
            predicted, prob_itm, data_date,
            "", "", "", "",
        ])

    print(f"\nLogged {symbol} ${strike} {option_type.upper()} expiring {expiration}:")
    print(f"  Helium predicted_price: ${predicted}")
    print(f"  Helium prob_itm:        {prob_itm}")
    print(f"  Helium data date:       {data_date}")
    print(f"\nRow written to {LOG_FILE.resolve()}.")
    print("Fill in market_mark now (lookup elsewhere) and realized_itm after expiration")
    print("to compute the Brier loss for this contract.")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python 02_options_calibration_tracker.py SYMBOL STRIKE YYYY-MM-DD call|put")
        sys.exit(1)
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
