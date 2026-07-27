from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import analyze
from .providers import DemoMarketData, GoogleNewsRss, YahooChartData
from .report import render


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate explainable stock research notes.")
    parser.add_argument("--symbols", required=True, help="Comma-separated symbols, e.g. AAPL,MSFT")
    parser.add_argument("--demo", action="store_true", help="Use deterministic offline price data")
    parser.add_argument("--live", action="store_true", help="Fetch public Yahoo Finance chart data")
    parser.add_argument("--news", action="store_true", help="Fetch public Google News RSS headlines")
    parser.add_argument("--output", default="reports", help="Report directory")
    args = parser.parse_args()
    if args.demo == args.live:
        parser.error("Select exactly one of --demo or --live.")
    provider = DemoMarketData() if args.demo else YahooChartData()
    output = Path(args.output); output.mkdir(parents=True, exist_ok=True)
    for symbol in (item.strip() for item in args.symbols.split(",") if item.strip()):
        headlines = GoogleNewsRss().search(symbol) if args.news else []
        report = render(analyze(symbol, provider.history(symbol), headlines), headlines)
        target = output / f"{symbol.upper()}.md"; target.write_text(report, encoding="utf-8")
        print(f"Wrote {target}")


if __name__ == "__main__":
    main()

