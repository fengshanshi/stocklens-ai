from __future__ import annotations

from statistics import pstdev

from .models import NewsItem, PriceBar, Signal

POSITIVE = ("beat", "growth", "upgrade", "profit", "record", "surge", "gain")
NEGATIVE = ("miss", "lawsuit", "downgrade", "loss", "fraud", "cut", "risk")


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def analyze(symbol: str, bars: list[PriceBar], news: list[NewsItem] | None = None) -> Signal:
    if len(bars) < 21:
        raise ValueError("至少需要 21 个交易日的收盘价")
    closes = [bar.close for bar in bars]
    short, long = _mean(closes[-10:]), _mean(closes[-20:])
    change_20d = (closes[-1] / closes[-21] - 1) * 100
    returns = [(b / a - 1) * 100 for a, b in zip(closes[-21:-1], closes[-20:])]
    volatility = pstdev(returns)
    score, reasons = 50, []
    if short > long:
        score += 18; trend = "上行"; reasons.append("10日均价高于20日均价")
    else:
        score -= 18; trend = "下行"; reasons.append("10日均价低于20日均价")
    if change_20d > 5:
        score += 12; momentum = "强"; reasons.append(f"20日涨幅 {change_20d:.1f}%")
    elif change_20d < -5:
        score -= 12; momentum = "弱"; reasons.append(f"20日跌幅 {change_20d:.1f}%")
    else:
        momentum = "中性"; reasons.append(f"20日变动 {change_20d:.1f}%")
    if volatility > 3:
        score -= 10; volatility_label = "高"; reasons.append(f"日波动率 {volatility:.2f}%：较高")
    else:
        volatility_label = "正常"; reasons.append(f"日波动率 {volatility:.2f}%")
    headlines = " ".join(item.title.lower() for item in news or [])
    sentiment = sum(word in headlines for word in POSITIVE) - sum(word in headlines for word in NEGATIVE)
    if sentiment:
        score += max(-8, min(8, sentiment * 2)); reasons.append(f"新闻标题词倾向 {'正面' if sentiment > 0 else '负面'}（仅作线索）")
    score = max(0, min(100, score))
    stance = "偏多" if score >= 65 else "偏空" if score <= 35 else "观察"
    return Signal(symbol.upper(), score, stance, trend, momentum, volatility_label, tuple(reasons))

