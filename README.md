# StockLens AI

一个独立实现的股票研究工作台：聚合行情与新闻，计算可解释的技术信号，并生成可复核的 Markdown 研究报告。

> 仅供学习与研究，不构成投资建议。数据可能延迟、不完整或错误；请自行核验并独立决策。

## 当前 MVP

- 多标的批量研究：CLI 接受 `AAPL,MSFT` 这类列表
- 行情适配器：内置离线演示数据；可选接入 Yahoo Finance 图表 API
- 新闻适配器：可选 RSS 检索（默认关闭，避免意外网络请求）
- 可解释评分：趋势、动量、波动与新闻情绪分别评分，产生 `观察 / 偏多 / 偏空`
- Markdown 报告：保留原始来源链接、数据时间和风险提示

## 快速开始

```powershell
python -m stocklens --symbols AAPL,MSFT --demo
python -m stocklens --symbols AAPL --live --news --output reports
```

第二条命令会访问公开行情与 RSS 服务。首次运行无需 API 密钥。

## 项目结构

```text
stocklens/          核心领域逻辑与适配器
tests/              无网络的单元测试
reports/            生成的报告（已忽略）
```

## 后续接入

- 新市场数据源：实现 `MarketDataProvider` 协议
- LLM 摘要：在报告层添加提供商适配器，明确标注模型结论与原始事实
- 自动任务：可由 GitHub Actions 或任意调度器调用 CLI

## 开发

```powershell
python -m unittest discover -s tests -v
```

## 许可证

MIT。

