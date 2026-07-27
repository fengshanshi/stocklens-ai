from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PriceBar:
    timestamp: datetime
    close: float


@dataclass(frozen=True)
class NewsItem:
    title: str
    published_at: datetime | None
    url: str
    source: str


@dataclass(frozen=True)
class Signal:
    symbol: str
    score: int
    stance: str
    trend: str
    momentum: str
    volatility: str
    reasons: tuple[str, ...]

