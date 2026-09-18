---
name: california-polling-analysis
description: Analyze polling data for California gubernatorial elections, including aggregating poll sources, calculating weighted averages, interpreting trends, and forecasting outcomes for California's top-two primary system.
phases: [analysis, report]
---

# California Polling Analysis Skill

## Core Purpose
Provide a repeatable workflow to:

- Pull poll data from multiple aggregators (270toWin, RealClearPolitics, Decision Desk HQ, Race to the WH, FiftyPlusOne)
- Compute weighted averages and trend lines
- Adjust for pollster methodology, sample size, and margin of error
- Generate forecasts with confidence intervals
- Produce a concise report format suitable for stakeholders

## Required Inputs
- Raw poll data files (CSV/JSON) or URLs to poll aggregator endpoints
- Optional: historical election results for context

## Step‑by‑Step Workflow
1. **Collect**: Use `browser_navigate` → `browser_snapshot` → `read_file` to capture poll aggregator pages.
2. **Parse**: Extract poll tables via `read_file` with appropriate offsets; store as CSV in `temp/polls.csv`.
3. **Normalize**: Run a Python script (`scripts/normalize_polls.py`) to:
   - Convert dates to ISO format
   - Compute sample size weighting
   - Apply inverse‑variance weighting for margin‑of‑error
4. **Aggregate**: Execute `scripts/aggregate_polls.py` to produce:
   - Weighted average for each candidate
   - Trend line (linear regression over the last 30 days)
   - Forecast with 95% confidence interval
5. **Report**: Use `templates/report.md` as a markdown scaffold; populate with:
   - Current weighted averages
   - Trend snapshot (ASCII sparkline)
   - Forecast summary
   - Key assumptions and limitations

## Common Pitfalls
- **Single‑poll overreliance** – always aggregate; single polls can be outliers.
- **Methodology blind spots** – different aggregators use different weighting schemes; note discrepancies.
- **Top‑two primary blind spot** – treat the primary as a separate race; do not carry primary margins directly into the general‑election forecast.
- **Margin‑of‑error misinterpretation** – treat MoE as uncertainty, not as a hard cutoff.

## Usage Example
```bash
/skill california-polling-analysis run --input polls.csv --output report.md
```

## References
- references/california-polling-analysis.md