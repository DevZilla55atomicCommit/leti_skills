# Forex Skills — To Be Created

*The agent squad template references four Forex skills that don't exist yet. This file tracks their design for future creation.*

---

## 1. forex-technical-analysis

**Purpose**: Technical analysis patterns, indicators, and chart reading for FX markets.

**Scope**:
- Price action patterns (candlesticks, chart patterns)
- Support/Resistance identification
- Fibonacci retracements/extensions
- Moving averages (EMA, SMA, VWAP)
- Momentum oscillators (RSI, MACD, Stochastic)
- Volume analysis (where available)
- Wyckoff / Smart Money Concepts (order blocks, liquidity, market structure)
- Multi-timeframe analysis (HTF bias + LTF entry)

**Output Format**:
```json
{
  "pair": "EUR/USD",
  "timeframe": "4H",
  "bias": "bullish",
  "pattern": "break of structure + retest",
  "key_levels": {"support": [1.0850, 1.0800], "resistance": [1.0920, 1.0950]},
  "entry_zone": [1.0860, 1.0870],
  "invalidation": 1.0800,
  "targets": [1.0920, 1.0950, 1.1000],
  "confidence": 0.75
}
```

---

## 2. forex-macro-fundamentals

**Purpose**: Macro fundamental analysis for FX — central banks, economic data, geopolitical risk.

**Scope**:
- Central bank policy tracking (Fed, ECB, BoE, BoJ, RBA, BOC, SNB, RBNZ)
- Interest rate expectations (dot plots, OIS curves, forward guidance)
- Key economic indicators (CPI, PPI, NFP, GDP, PMI, retail sales, unemployment)
- Monetary policy divergence between currency pairs
- Geopolitical risk assessment (wars, elections, trade policy)
- Risk sentiment (risk-on/off, DXY correlation, yield spreads)
- Calendar management (FOMC, ECB, NFP, CPI dates)

**Output Format**:
```json
{
  "pair": "EUR/USD",
  "fundamental_bias": "bearish",
  "drivers": [
    {"factor": "Fed vs ECB rate differential", "impact": "USD positive", "horizon": "3-6 months"},
    {"factor": "Eurozone PMIs contracting", "impact": "EUR negative", "horizon": "1-3 months"}
  ],
  "upcoming_events": [
    {"date": "2026-08-22", "event": "Jackson Hole Symposium", "currency": "USD", "importance": "high"},
    {"date": "2026-08-29", "event": "Eurozone CPI Flash", "currency": "EUR", "importance": "high"}
  ],
  "conviction": 0.7
}
```

---

## 3. terminal-alerting

**Purpose**: Automated terminal-based alerting for FX conditions.

**Scope**:
- Price alerts (level breach, % move, volatility spike)
- Pattern alerts (candlestick patterns, breakouts)
- Indicator alerts (RSI extremes, MACD cross, MA cross)
- Calendar alerts (high-impact events, central bank speeches)
- Technical condition alerts (S/R test, trendline break)
- Multi-condition alerts (confluence of factors)

**Implementation**:
- Python scripts using `requests` + FX data APIs (Twelve Data, Alpha Vantage, or broker API)
- `cron` or `launchd` for scheduling
- Notification via: terminal bell, macOS notification (`osascript`), webhook (Discord/Slack/Telegram)
- Config file for alert rules (YAML/JSON)

**Example Alert Rule**:
```yaml
- name: "EUR/USD RSI Oversold 1H"
  pair: "EUR/USD"
  timeframe: "1H"
  condition: "rsi < 30"
  cooldown_minutes: 60
  notify: ["terminal", "macos"]
```

---

## 4. trading-journal

**Purpose**: Structured trade logging and review in Obsidian vault.

**Scope**:
- Trade entry logging (setup, entry, stop, targets, risk%, position size)
- Trade management (adjustments, partial exits, stops moved)
- Trade exit logging (exit price, P&L, R-multiple, lessons)
- Periodic review (weekly/monthly statistics, pattern analysis)
- Integration with Obsidian vault at `/Volumes/PNY128GBLED/TamaZila Obsidian Vault`

**Obsidian Structure**:
```
Trading Journal/
├── 2026/
│   ├── 2026-08-August.md
│   └── ...
├── Templates/
│   ├── trade-entry.md
│   ├── trade-exit.md
│   └── weekly-review.md
├── Statistics/
│   ├── 2026-Q3.md
│   └── ...
└── Setups/
    ├── breakout.md
    ├── pullback.md
    └── reversal.md
```

**Trade Entry Template**:
```markdown
---
date: 2026-08-19
pair: EUR/USD
direction: long
timeframe: 4H
setup: "break of structure + retest"
entry: 1.0865
stop: 1.0800
targets: [1.0920, 1.0950, 1.1000]
risk_pct: 1.5
position_size: 0.5 lots
conviction: 0.75
notes: "Aligns with daily bullish bias. ECB minutes dovish."
---
```

---

## Creation Priority

1. **forex-technical-analysis** — Core skill, used by every analysis
2. **forex-macro-fundamentals** — Core skill, pairs with technical
3. **trading-journal** — Infrastructure, enables review loop
4. **terminal-alerting** — Automation, can use existing cron/launchd skills as base

---

## Integration with Existing Skills

- `data-science/jupyter-live-kernel` — For backtesting, indicator calculation
- `visualization/benchmark-visualization` — For equity curves, performance charts
- `cron-job-validation` — For alert scheduler reliability
- `macos-launch-agent-management` — For persistent background alerting
- `obsidian` / `note-taking` — For journal storage in vault