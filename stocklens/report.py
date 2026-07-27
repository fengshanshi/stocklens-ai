from __future__ import annotations

from datetime import datetime

from .models import NewsItem, Signal


def render(signal: Signal, news: list[NewsItem]) -> str:
    lines = [f"# {signal.symbol} 研究快报", "", f"> 生成时间：{datetime.now().astimezone().isoformat(timespec='minutes')}", "", "## 信号摘要", "", f"- 综合分：**{signal.score}/100**", f"- 立场：**{signal.stance}**（非交易建议）", f"- 趋势：{signal.trend}；动量：{signal.momentum}；波动：{signal.volatility}", "", "## 可复核依据", ""]
    lines.extend(f"- {reason}" for reason in signal.reasons)
    lines.extend(["", "## 新闻线索", ""])
    if news:
        for item in news:
            lines.append(f"- [{item.title}]({item.url}) — {item.source}")
    else:
        lines.append("- 本次未启用新闻检索。")
    lines.extend(["", "## 风险提示", "", "- 该报告基于公开数据与简单规则，可能滞后或失真。", "- 不包含估值、财务质量、流动性、持仓约束或个人风险承受能力。", "- 请核对原始来源；本项目不提供买卖建议。", ""])
    return "\n".join(lines)

