from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Protocol

from .models import NewsItem, PriceBar


class MarketDataProvider(Protocol):
    def history(self, symbol: str, days: int = 90) -> list[PriceBar]: ...


class DemoMarketData:
    """Deterministic local prices used for safe demos and tests."""
    def history(self, symbol: str, days: int = 90) -> list[PriceBar]:
        base = 100 + (sum(map(ord, symbol.upper())) % 35)
        start = datetime.now(UTC) - timedelta(days=days)
        return [PriceBar(start + timedelta(days=i), round(base + i * 0.22 + ((i % 7) - 3) * 0.45, 2)) for i in range(days)]


class YahooChartData:
    """Small public-data adapter. It does not require or store credentials."""
    def history(self, symbol: str, days: int = 90) -> list[PriceBar]:
        query = urllib.parse.urlencode({"range": f"{days}d", "interval": "1d"})
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?{query}"
        request = urllib.request.Request(url, headers={"User-Agent": "StockLensAI/0.1 (research tool)"})
        with urllib.request.urlopen(request, timeout=12) as response:
            payload = json.load(response)["chart"]["result"][0]
        closes = payload["indicators"]["quote"][0]["close"]
        return [PriceBar(datetime.fromtimestamp(ts, UTC), float(close)) for ts, close in zip(payload["timestamp"], closes) if close is not None]


class GoogleNewsRss:
    def search(self, symbol: str, limit: int = 5) -> list[NewsItem]:
        query = urllib.parse.quote(f"{symbol} stock")
        request = urllib.request.Request(f"https://news.google.com/rss/search?q={query}", headers={"User-Agent": "StockLensAI/0.1"})
        with urllib.request.urlopen(request, timeout=12) as response:
            root = ET.fromstring(response.read())
        items: list[NewsItem] = []
        for node in root.findall("./channel/item")[:limit]:
            raw_date = node.findtext("pubDate")
            items.append(NewsItem(node.findtext("title", "Untitled"), parsedate_to_datetime(raw_date) if raw_date else None, node.findtext("link", ""), node.findtext("source", "Google News")))
        return items

